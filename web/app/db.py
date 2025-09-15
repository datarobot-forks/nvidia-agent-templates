# Copyright  DataRobot, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
from contextlib import asynccontextmanager
from functools import wraps
from typing import AsyncGenerator, ParamSpec, TypeVar, Protocol, Generic, Callable, Coroutine, Concatenate, cast

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from core.persistent_fs.dr_file_system import DRFileSystem, calculate_checksum


def _prepare_persistence_storage(
    engine: AsyncEngine,
) -> tuple[DRFileSystem, str] | tuple[None, None]:
    # check if all env variables are present
    expected_envs = ["DATAROBOT_ENDPOINT", "DATAROBOT_API_TOKEN", "APPLICATION_ID"]
    if any(not os.environ.get(env_name) for env_name in expected_envs):
        return None, None

    if "sqlite" not in engine.url.drivername:
        return None, None
    if not engine.url.database or ":memory:" == engine.url.database:
        return None, None

    file_path = engine.url.database
    persistent_fs = DRFileSystem()
    return persistent_fs, file_path


class DBCtx:
    def __init__(self, engine: AsyncEngine):
        self.engine = engine

        self._session = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            class_=AsyncSession,
            bind=engine,
            expire_on_commit=False,
        )

        self._persistence_fs: DRFileSystem | None
        self._db_path: str | None
        self._persistence_fs, self._db_path = _prepare_persistence_storage(engine)

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        checksum: bytes | None = None
        if self._persistence_fs and self._persistence_fs.exists(self._db_path):
            self._persistence_fs.get(self._db_path, self._db_path)
            checksum = calculate_checksum(cast(str, self._db_path))

        async with self._session() as session:
            yield session

        if self._persistence_fs:
            new_checksum = calculate_checksum(cast(str, self._db_path))
            if new_checksum != checksum:
                self._persistence_fs.put(self._db_path, self._db_path)

    async def shutdown(self) -> None:
        """
        Dispose of the engine and close all pooled connections.
        Call this on application shutdown.
        """
        await self.engine.dispose()


P = ParamSpec("P")
T = TypeVar("T", covariant=True)


class Repository(Protocol):
    @property
    def _db(self) -> DBCtx:
        ...


R = TypeVar("R", bound=Repository)


def retry_on_integrity_error(
    f: Callable[Concatenate[R, AsyncSession, P], Coroutine[None, None, T]],
    retry_count: int = 3
) -> Callable[Concatenate[R, P], Coroutine[None, None, T]]:
    """
    A decorator for a method of a repository that
    1. Wraps the method in a session (closing/aborting the session).
    2. Retries the method up to `retry_count` times if it errors out.

    The use case of this decorator is to smooth over gaps in SQLite's transactions/constraints
    compared to other DBs: upserts that are nice and atomic in e.g. Postgres are not so by
    default in SQLite. (And the way to accomplish this, with `BEGIN (IMMEDIATE|EXCLUSIVE)`
    ransactions is likely to cause locking issue because of SQLite's full-DB locks, so retries
    can be the lesser of two evils.)
    """
    if retry_count < 0:
        raise ValueError("retry_count must be non-negative.")

    @wraps(f)
    async def inner(self: R, *args: P.args, **kwargs: P.kwargs) -> T:
        async with self._db.session() as sess:
            attempt = 0
            while True:
                attempt += 1
                try:
                    return await f(self, sess, *args, **kwargs)
                except IntegrityError as e:
                    await sess.rollback()
                    if attempt == retry_count:
                        raise

    return inner


async def create_db_ctx(db_url: str, log_sql_stmts: bool = False) -> DBCtx:
    async_engine = create_async_engine(
        db_url,
        echo=log_sql_stmts,
    )

    async with async_engine.begin() as conn:
        # testing DB credentials...
        await conn.execute(text("select '1'"))

        await conn.run_sync(
            SQLModel.metadata.create_all
        )  # create_all is a blocking method

    return DBCtx(async_engine)
