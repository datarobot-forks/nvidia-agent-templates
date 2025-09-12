# Copyright 2025 DataRobot, Inc.
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
import json
import logging
import uuid as uuidpkg
from functools import lru_cache
from typing import TYPE_CHECKING, Any

import datarobot as dr
from datarobot.auth.session import AuthCtx
from datarobot.auth.typing import Metadata
from datarobot.client import RESTClientObject
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from openai import AsyncOpenAI
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_system_message_param import (
    ChatCompletionSystemMessageParam,
)
from openai.types.chat.chat_completion_user_message_param import (
    ChatCompletionUserMessageParam,
)
from pydantic import ValidationError
from sqlalchemy.exc import NoResultFound

from app.auth.ctx import must_get_auth_ctx
from app.models.chats import Chat, ChatCreate, ChatRepository
from app.models.messages import Message, MessageCreate, MessageRepository, Role
from app.api.v1.schema import ChatCompletionRequest
from core import getenv

if TYPE_CHECKING:
    from app.users.user import User, UserRepository

logger = logging.getLogger(__name__)

chat_router = APIRouter(tags=["Chat"])

agent_deployment_url = getenv("AGENT_DEPLOYMENT_URL") or ""
agent_deployment_token = getenv("AGENT_DEPLOYMENT_TOKEN") or "dummy"


SYSTEM_PROMPT = (
    "You are a helpful assistant. Use the provided document(s) to answer "
    "as accurately as possible. If the answer is not contained in the documents, "
    "say you don't know. When documents have page numbers, you can reference "
    "specific pages and their filenames in your answer."
)


@lru_cache(maxsize=128)
def initialize_deployment(deployment_id: str) -> tuple[RESTClientObject, str]:
    try:
        dr_client = dr.Client()

        deployment_chat_base_url = dr_client.endpoint + f"/deployments/{deployment_id}/"
        return dr_client, deployment_chat_base_url
    except ValidationError as e:
        raise ValueError(
            "Unable to load Deployment ID."
            "If running locally, verify you have selected the correct "
            "stack and that it is active using `pulumi stack output`. "
            "If running in DataRobot, verify your runtime parameters have been set correctly."
        ) from e


async def _get_current_user(user_repo: "UserRepository", user_id: int) -> "User":
    current_user = await user_repo.get_user(user_id=user_id)
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    return current_user


def _format_chat(chat: Chat, message: Message | None) -> dict[str, Any]:
    data = chat.dump_json_compatible()
    if message:
        message_data = message.dump_json_compatible()
        data["updated_at"] = message_data["created_at"]
        data["model"] = message_data["model"]
    else:
        data["updated_at"] = data["created_at"]
        data["model"] = None
    return data


async def _get_or_create_chat_id(
    chat_repo: ChatRepository, chat_id: str | None, current_user: "User"
) -> tuple[uuidpkg.UUID, bool]:
    """
    Get or create a chat ID. Returns tuple of (chat_uuid, was_created).
    """
    # If no chat_id provided, create new chat
    if not chat_id:
        new_chat = await chat_repo.create_chat(
            ChatCreate(name="New Chat", user_uuid=current_user.uuid)
        )
        return new_chat.uuid, True

    # Try to parse the chat_id as UUID
    try:
        uuid_value = uuidpkg.UUID(chat_id)
    except ValueError:
        # Invalid UUID format, create new chat
        new_chat = await chat_repo.create_chat(
            ChatCreate(name="New Chat", user_uuid=current_user.uuid)
        )
        return new_chat.uuid, True

    # Check if chat exists
    try:
        await chat_repo.get_chat(uuid_value)
        return uuid_value, False
    except NoResultFound:
        # Chat doesn't exist, create new chat
        new_chat = await chat_repo.create_chat(
            ChatCreate(name="New Chat", user_uuid=current_user.uuid)
        )
        return new_chat.uuid, True


@chat_router.post("/chat/completions")
async def chat_completion(
    request_data: ChatCompletionRequest,
    request: Request,
    auth_ctx: AuthCtx[Metadata] = Depends(must_get_auth_ctx)
) -> Any:
    # Extract parameters from request body
    message = request_data.message
    model = request_data.model
    chat_id = request_data.chat_id
    
    # Get current user's UUID
    current_user = await _get_current_user(
        request.app.state.deps.user_repo, int(auth_ctx.user.id)
    )

    # Get repositories
    chat_repo: ChatRepository = request.app.state.deps.chat_repo
    message_repo: MessageRepository = request.app.state.deps.message_repo

    # Get the correct chat
    chat_uuid, _ = await _get_or_create_chat_id(chat_repo, chat_id, current_user)
    await message_repo.create_message(
        MessageCreate(
            chat_id=chat_uuid,
            role=Role.USER,
            model=model,
            content=message,
            components="",
            error=None,
        )
    )

    dr_client, deployment_chat_base_url = initialize_deployment(
        request.app.state.deps.config.llm_deployment_id
    )
    openai_client = AsyncOpenAI(
        api_key=dr_client.token,
        base_url=deployment_chat_base_url,
        timeout=90,
        max_retries=2,
    )

    # Create OpenAI messages
    messages: list[ChatCompletionMessageParam] = [
        ChatCompletionSystemMessageParam(role="system", content=SYSTEM_PROMPT),
        ChatCompletionUserMessageParam(role="user", content=message),
    ]

    async with openai_client as client:
        completion = await client.chat.completions.create(
            model=model,
            messages=messages,
        )
    llm_message_content = completion.choices[0].message.content
    response_message = await message_repo.create_message(
        MessageCreate(
            chat_id=chat_uuid,
            role=Role.ASSISTANT,
            model=model,
            content=llm_message_content or "",
            components="",
            error=None,
        )
    )
    return JSONResponse(content=response_message.dump_json_compatible())


@chat_router.post("/chat/agent/completions")
async def chat_agent_completion(
    request_data: ChatCompletionRequest,
    request: Request,
    auth_ctx: AuthCtx[Metadata] = Depends(must_get_auth_ctx)
) -> Any:
    # Get current user's UUID
    current_user = await _get_current_user(
        request.app.state.deps.user_repo, int(auth_ctx.user.id)
    )

    message = request_data.message
    llm_model = request_data.model
    chat_id = request_data.chat_id or None

    chat_repo: ChatRepository = request.app.state.deps.chat_repo
    message_repo: MessageRepository = request.app.state.deps.message_repo

    chat_id, _ = await _get_or_create_chat_id(
        chat_repo, chat_id, current_user
    )
    await message_repo.create_message(
        MessageCreate(
            chat_id=chat_id,
            role=Role.USER,
            model=llm_model,
            content=message,
            components="",
            error=None,
        )
    )
    if agent_deployment_url:
        # If the agent deployment URL is provided, use it directly
        deployment_chat_base_url = agent_deployment_url
        token = agent_deployment_token
    else:
        dr_client, deployment_chat_base_url = initialize_deployment(
            request.app.state.deps.config.agent_retrieval_agent_deployment_id
        )
        token = dr_client.token
    openai_client = AsyncOpenAI(
        api_key=token,
        base_url=deployment_chat_base_url,
        timeout=90,
        max_retries=2,
    )
    # Create OpenAI formatted for Crew AI
    content: dict[str, Any] = {
        "topic": "documentation",
        "question": f"{message}",
    }

    messages: list[ChatCompletionMessageParam] = [
        ChatCompletionUserMessageParam(role="user", content=json.dumps(content)),
    ]
    async with openai_client as client:
        completion = await client.chat.completions.create(
            model=llm_model,
            messages=messages,
        )
    llm_message_content = completion.choices[0].message.content or ""
    response_message = await message_repo.create_message(
        MessageCreate(
            chat_id=chat_id,
            role=Role.ASSISTANT,
            model=llm_model,
            content=llm_message_content,
            components="",
            error=None,
        )
    )
    return JSONResponse(content=response_message.dump_json_compatible())


@chat_router.get("/chat/llm/catalog")
def get_available_llm_catalog(request: Request) -> Any:
    dr_client, _ = initialize_deployment(
        request.app.state.deps.config.llm_deployment_id
    )

    response = dr_client.get("genai/llmgw/catalog/")
    data = response.json()
    return JSONResponse(content=data)


@chat_router.get("/chat")
async def get_list_of_chats(
    request: Request, auth_ctx: AuthCtx[Metadata] = Depends(must_get_auth_ctx)
) -> Any:
    """Return list of all chats"""
    # Get current user's UUID
    current_user = await _get_current_user(
        request.app.state.deps.user_repo, int(auth_ctx.user.id)
    )

    chat_repo = request.app.state.deps.chat_repo
    message_repo = request.app.state.deps.message_repo

    chats = await chat_repo.get_all_chats(current_user)
    chat_ids = [chat.uuid for chat in chats]
    last_messages = await message_repo.get_last_messages(chat_ids)

    return JSONResponse(
        content=[_format_chat(chat, last_messages.get(chat.uuid)) for chat in chats]
    )


@chat_router.get("/chat/{chat_uuid}")
async def get_chat(request: Request, chat_uuid: uuidpkg.UUID) -> Any:
    """Return info about a specific chat"""
    chat_repo = request.app.state.deps.chat_repo
    message_repo = request.app.state.deps.message_repo

    chat = await chat_repo.get_chat(chat_uuid)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="chat not found"
        )

    last_message = await message_repo.get_last_messages([chat.uuid])

    return JSONResponse(content=_format_chat(chat, last_message.get(chat.uuid)))


@chat_router.patch("/chat/{chat_uuid}")
async def update_chat(request: Request, chat_uuid: uuidpkg.UUID) -> Any:
    """Updates chat name.
    Payload:
    name: str name of chat
    """
    chat_repo = request.app.state.deps.chat_repo
    request_data = await request.json()
    new_name = request_data.get("name")
    if not new_name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="name is absent or empty",
        )
    chat = await chat_repo.update_chat_name(chat_uuid, new_name)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="chat not found"
        )
    return JSONResponse(content=chat.dump_json_compatible())


@chat_router.delete("/chat/{chat_uuid}")
async def delete_chat(request: Request, chat_uuid: uuidpkg.UUID) -> Any:
    """Deletes a chat."""
    chat_repo = request.app.state.deps.chat_repo
    chat = await chat_repo.delete_chat(chat_uuid)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="chat not found"
        )
    return JSONResponse(content=chat.dump_json_compatible())


@chat_router.get("/chat/{chat_uuid}/messages")
async def get_chat_messages(request: Request, chat_uuid: uuidpkg.UUID) -> Any:
    """Return list of all chats"""
    message_repo = request.app.state.deps.message_repo
    messages = await message_repo.get_chat_messages(chat_uuid)
    return JSONResponse(content=[m.dump_json_compatible() for m in messages])
