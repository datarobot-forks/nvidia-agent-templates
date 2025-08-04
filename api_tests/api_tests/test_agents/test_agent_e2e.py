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
import os

from api_tests.api_tests.test_agents.helpers import AgentE2EHelper


def test_local_environment_variables():
    # Ensure the required environment variables are set
    print("Checking environment variables (root .env file)")

    required_vars = [
        "DATAROBOT_API_TOKEN",
        "DATAROBOT_ENDPOINT",
    ]
    for var in required_vars:
        assert os.getenv(var), (
            f"Environment variable {var} is not set, please set it in the .env file"
        )


def test_e2e_agent_crewai(
    root_path,
    repo_path,
):
    print("Running agent_crewai E2E agent test")
    agent_helper = AgentE2EHelper(
        agent_name="agent_crewai",
        repo_path=repo_path,
    )
    agent_helper.run()


def test_e2e_agent_base(
    root_path,
    repo_path,
):
    print("Running agent_generic_base E2E agent test")
    agent_helper = AgentE2EHelper(
        agent_name="agent_generic_base",
        repo_path=repo_path,
    )
    agent_helper.run()


def test_e2e_agent_langgraph(
    root_path,
    repo_path,
):
    print("Running agent_langgraph E2E agent test")
    agent_helper = AgentE2EHelper(
        agent_name="agent_langgraph",
        repo_path=repo_path,
    )
    agent_helper.run()


def test_e2e_agent_llamaindex(
    root_path,
    repo_path,
):
    print("Running agent_llamaindex E2E agent test")
    agent_helper = AgentE2EHelper(
        agent_name="agent_llamaindex",
        repo_path=repo_path,
    )
    agent_helper.run()
