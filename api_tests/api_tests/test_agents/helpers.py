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
import os
import subprocess
import time
from typing import cast, Union

import requests

UV_COMMAND = os.environ.get("UV_COMMAND", "uv")
TASKFILE_COMMAND = os.environ.get("TASKFILE_COMMAND", "task")


def fprint(msg: Union[str, list[str]]):
    print(msg, flush=True)


class AgentE2EHelper:
    def __init__(
        self,
        agent_name=None,
        repo_path=None,
    ):
        self.agent_name = agent_name
        self.repo_path = repo_path

    def run(self):
        if len(os.environ.get("DATAROBOT_DEFAULT_EXECUTION_ENVIRONMENT", "")) > 0:
            print(
                "⚠️ WARNING: DATAROBOT_DEFAULT_EXECUTION_ENVIRONMENT is set, "
                "this will use a pre-existing environment. ⚠️"
            )
        try:
            self.pulumi_create_stack()
            self.run_local_execution("Artificial Intelligence")
            custom_model_id = self.pulumi_build_agent()
            self.retry_on_failure(
                self.run_custom_model_execution,
                max_retries=3,
                delay=30,
                user_prompt="Artificial Intelligence",
                custom_model_id=custom_model_id,
            )
            deployment_id = self.pulumi_deploy_agent()
            self.retry_on_failure(
                self.run_deployment_execution,
                max_retries=3,
                delay=30,
                user_prompt="Artificial Intelligence",
                deployment_id=deployment_id,
            )
            print("Agent execution completed successfully")
        finally:
            self.cleanup_environment()

    @staticmethod
    def run_process(command, directory, env=None):
        process = subprocess.Popen(
            command,
            env=env,
            encoding="utf-8",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            cwd=directory,
        )

        # Collect output while displaying it in real-time
        output_lines = []
        for line in iter(process.stdout.readline, ""):
            line = line.rstrip("\n")
            if line:  # Only print non-empty lines
                print(line, flush=True)
                output_lines.append(line)

        # Wait for process to complete and check return code
        return_code = process.wait()
        if return_code != 0:
            raise subprocess.CalledProcessError(return_code, command)

        # Return the collected output as a single string, similar to check_output
        return "\n".join(output_lines)

    def destroy_environment(self, timeout=600):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                self.run_process(
                    [f"pulumi destroy -s {self.agent_name} -f -y"],
                    os.path.join(self.repo_path, "infra"),
                )
                # If successful, exit the function
                return
            except subprocess.CalledProcessError as e:
                elapsed_time = time.time() - start_time
                remaining_time = timeout - elapsed_time

                if remaining_time <= 30:
                    # Not enough time for another retry
                    fprint(f"Destroy could not complete within timeout: {e}")
                    return

                fprint(f"Destroy failed, retrying in 30 seconds... ({e})")
                time.sleep(30)

        # If we exit the loop, timeout was reached
        fprint("Destroy could not complete: timeout reached")

    def cleanup_environment(self):
        fprint("CLEANING UP LOCAL AND REMOTE ENVIRONMENT")
        fprint("========================================")
        # Attempt to destroy the stack
        fprint("Cancelling any running Pulumi operations for agent")
        try:
            self.run_process(
                [f"pulumi cancel -s {self.agent_name} -y"],
                os.path.join(self.repo_path, "infra"),
            )
        except subprocess.CalledProcessError as e:
            fprint(f"Destroy could not complete: {e}")

        fprint("Destroying Pulumi stack for agent")
        self.destroy_environment(timeout=600)

        fprint("Removing Pulumi stack for agent")
        try:
            self.run_process(
                [f"pulumi stack rm -s {self.agent_name} -f -y"],
                os.path.join(self.repo_path, "infra"),
            )
        except subprocess.CalledProcessError as e:
            fprint(f"Stack does not exist: {e}")
        fprint("CLEAN UP COMPLETED")

    def pulumi_create_stack(self):
        fprint("Creating Pulumi stack for agent")
        fprint("===============================")
        try:
            self.run_process(
                [f"pulumi stack rm -s {self.agent_name} -f -y"],
                os.path.join(self.repo_path, "infra"),
            )
        except subprocess.CalledProcessError as e:
            fprint("Ignoring deletion error, stack may not exist during setup")
            fprint(f"Stack does not exist: {e}")

        self.run_process(
            ["export PULUMI_ACCESS_TOKEN=123 && pulumi login --local"],
            os.path.join(self.repo_path, "infra"),
        )

        result = self.run_process(
            [f"pulumi stack init -s {self.agent_name}"],
            os.path.join(self.repo_path, "infra"),
        )
        assert "Created stack" in result

    def pulumi_build_agent(self):
        fprint("Running Pulumi up to build the agent")
        fprint("====================================")
        result = self.run_process(
            ["task build -- --yes"],
            os.path.join(self.repo_path, "infra"),
        )
        custom_model_rows = [
            row
            for row in result.split("\n")
            if f"Custom Model ID [{self.agent_name}]" in row
        ]
        custom_model_id = custom_model_rows[-1].split('"')[-2]
        fprint(f"Custom model ID: {custom_model_id}")
        return custom_model_id

    def pulumi_deploy_agent(self):
        fprint("Running Pulumi up to deploy the agent")
        fprint("=====================================")
        result = self.run_process(
            [f"export AGENT_DEPLOY=1 && pulumi up -y -s {self.agent_name}"],
            os.path.join(self.repo_path, "infra"),
        )
        deployment_rows = [
            row
            for row in result.split("\n")
            if f"Agent Deployment ID [{self.agent_name}]" in row
        ]
        deployment_id = deployment_rows[-1].split('"')[-2]
        fprint(f"Agent deployment ID: {deployment_id}")
        return deployment_id

    def run_local_execution(self, user_prompt: str):
        fprint("Running local agent execution")
        fprint("=============================")
        result = self.run_process(
            [f'{TASKFILE_COMMAND} agent:cli -- execute --user_prompt "{user_prompt}"'],
            self.repo_path,
        )

        # Verify the OpenAI Response
        result = cast(str, result)
        local_result = json.loads(result.split("Stored Execution Result:")[-1])
        assert [
            key in local_result
            for key in [
                "id",
                "choices",
                "created",
                "model",
                "object",
                "usage",
                "pipeline_interactions",
            ]
        ]
        assert len(local_result["choices"]) == 1
        fprint("Valid agent response")

    def run_custom_model_execution(self, user_prompt: str, custom_model_id: str):
        fprint("Running custom model agent execution")
        fprint("====================================")
        headers = {
            "Authorization": f"Bearer {os.environ['DATAROBOT_API_TOKEN']}",
            "Content-Type": "application/json",
        }
        data = {"messages": [{"role": "user", "content": user_prompt}]}

        fprint("POST to custom model agent endpoint")
        response = requests.post(
            f"{os.environ['DATAROBOT_ENDPOINT']}/genai/agents/fromCustomModel/{custom_model_id}/chat/",
            headers=headers,
            json=data,
        )
        # Something wrong
        if not response.ok or not response.headers.get("Location"):
            raise Exception(response.content)
        fprint("Agent execution started, waiting for completion...")
        # Wait for the agent to complete
        status_location = response.headers["Location"]
        last_update_time = time.time()

        while response.ok:
            time.sleep(1)
            response = requests.get(
                status_location, headers=headers, allow_redirects=False
            )

            # Show update every 10 seconds
            current_time = time.time()
            if current_time - last_update_time >= 5:
                fprint("Agent execution still in progress...")
                last_update_time = current_time

            if response.status_code == 303:
                fprint("Agent execution completed, fetching response...")
                agent_response = requests.get(
                    response.headers["Location"], headers=headers
                ).json()
                # Show the agent response
                break
            else:
                status_response = response.json()
                if status_response["status"] in ["ERROR", "ABORTED"]:
                    raise Exception(status_response)
        else:
            raise Exception(response.content)

        assert "choices" in agent_response, "No choices in agent response"
        fprint("Valid agent response:")
        fprint(agent_response)

    def run_deployment_execution(self, user_prompt: str, deployment_id: str):
        fprint("Running deployed agent execution")
        fprint("================================")
        deployment_result = self.run_process(
            [
                f'{TASKFILE_COMMAND} agent:cli -- execute-deployment --user_prompt "{user_prompt}" --deployment_id {deployment_id}'
            ],
            self.repo_path,
        )

        # Assert there is a chat completion in the response
        deployment_result = cast(str, deployment_result)

        outputs = deployment_result.split("\n")
        assert "Running CLI execute-deployment" in outputs[0]
        assert len(outputs[5].split(", ")) > 10
        assert outputs[5].split(", ")[1] == "choices=[Choice(finish_reason='stop'"
        assert outputs[5].split(", ")[2] == "index=0"

        fprint("Valid agent response")

    def retry_on_failure(self, func, max_retries=3, delay=30, *args, **kwargs):
        """
        Retry a function up to max_retries times if it fails.

        Args:
            func: The function to retry
            max_retries: Maximum number of retry attempts (default: 3)
            delay: Delay between retries in seconds (default: 30)
            *args: Positional arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function

        Returns:
            The return value of the successful function call

        Raises:
            The last exception if all retry attempts fail
        """
        last_exception = None

        for attempt in range(max_retries + 1):  # +1 to include the initial attempt
            try:
                fprint(
                    f"Attempting {func.__name__} (attempt {attempt + 1}/{max_retries + 1})"
                )
                result = func(*args, **kwargs)
                if attempt > 0:
                    fprint(f"{func.__name__} succeeded on attempt {attempt + 1}")
                return result
            except Exception as e:
                last_exception = e
                if attempt < max_retries:
                    fprint(f"{func.__name__} failed on attempt {attempt + 1}: {e}")
                    fprint(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    fprint(
                        f"{func.__name__} failed on final attempt {attempt + 1}: {e}"
                    )

        # If we get here, all attempts failed
        raise last_exception
