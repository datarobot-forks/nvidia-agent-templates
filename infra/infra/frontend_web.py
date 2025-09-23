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

import pulumi
import pulumi_command as command
import time
from pathlib import Path
from datarobot_pulumi_utils.pulumi.stack import PROJECT_NAME

project_dir = Path(__file__).parent.parent.parent


def build_frontend():
    """
    Build the frontend application before deploying infrastructure.
    Split into two stages: install dependencies and build application.
    """
    frontend_dir = project_dir / "frontend_web"

    build_react_app = command.local.Command(
        f" [{PROJECT_NAME}] Build Frontend",
        create=f"cd {frontend_dir} && npm install && npm run build",
        triggers=[str(time.time())],  # This will cause rebuild every time
        opts=pulumi.ResourceOptions(
            # This resource should be created first
            depends_on=[]
        ),
    )

    return build_react_app


frontend_web = build_frontend()

__all__ = ["frontend_web"]
