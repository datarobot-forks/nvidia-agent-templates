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
import re
from typing import Any, Optional, Union

from helpers import create_inputs_from_completion_params
from langchain_community.chat_models import ChatLiteLLM
from langchain_core.messages import HumanMessage
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.graph.state import CompiledGraph, CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command
from openai.types.chat import CompletionCreateParams
from tools import list_drive_files_tool


class MyAgent:
    """MyAgent is a custom agent that uses Langgraph to plan, write, and edit content.
    It utilizes DataRobot's LLM Gateway or a specific deployment for language model interactions.
    This example illustrates 3 agents that handle content creation tasks, including planning, writing,
    and editing blog posts.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        model: Optional[str] = None,
        verbose: Optional[Union[bool, str]] = True,
        timeout: Optional[int] = 90,
        google_token: str = "",
        **kwargs: Any,
    ):
        """Initializes the MyAgent class with API key, base URL, model, and verbosity settings.

        Args:
            api_key: Optional[str]: API key for authentication with DataRobot services.
                Defaults to None, in which case it will use the DATAROBOT_API_TOKEN environment variable.
            api_base: Optional[str]: Base URL for the DataRobot API.
                Defaults to None, in which case it will use the DATAROBOT_ENDPOINT environment variable.
            model: Optional[str]: The LLM model to use.
                Defaults to None.
            verbose: Optional[Union[bool, str]]: Whether to enable verbose logging.
                Accepts boolean or string values ("true"/"false"). Defaults to True.
            timeout: Optional[int]: How long to wait for the agent to respond.
                Defaults to 90 seconds.
            **kwargs: Any: Additional keyword arguments passed to the agent.
                Contains any parameters received in the CompletionCreateParams.

        Returns:
            None
        """
        self.api_key = api_key or os.environ.get("DATAROBOT_API_TOKEN")
        self.api_base = api_base or os.environ.get("DATAROBOT_ENDPOINT")
        self.model = model
        self.timeout = timeout
        self.google_token = google_token
        if isinstance(verbose, str):
            self.verbose = verbose.lower() == "true"
        elif isinstance(verbose, bool):
            self.verbose = verbose

    @property
    def api_base_litellm(self) -> str:
        """Returns a modified version of the API base URL suitable for LiteLLM.

        Strips 'api/v2/' or 'api/v2' from the end of the URL if present.

        Returns:
            str: The modified API base URL.
        """
        if self.api_base:
            return re.sub(r"api/v2/?$", "", self.api_base)
        return "https://api.datarobot.com"

    @property
    def llm_with_datarobot_llm_gateway(self) -> ChatLiteLLM:
        """Returns a ChatLiteLLM instance configured to use DataRobot's LLM Gateway.

        This property can serve as a primary LLM backend for the agents. You can optionally
        have multiple LLMs configured, such as one for DataRobot's LLM Gateway
        and another for a specific DataRobot deployment, or even multiple deployments or
        third-party LLMs.
        """
        return ChatLiteLLM(
            model="datarobot/azure/gpt-4o-mini",
            api_base=self.api_base_litellm,
            api_key=self.api_key,
            timeout=self.timeout,
        )

    @property
    def llm_with_datarobot_deployment(self) -> ChatLiteLLM:
        """Returns a ChatLiteLLM instance configured to use DataRobot's LLM Deployments.

        This property can serve as a primary LLM backend for the agents. You can optionally
        have multiple LLMs configured, such as one for DataRobot's LLM Gateway
        and another for a specific DataRobot deployment, or even multiple deployments or
        third-party LLMs.
        """
        deployment_url = f"{self.api_base}/deployments/{os.environ.get('LLM_DATAROBOT_DEPLOYMENT_ID')}/"
        return ChatLiteLLM(
            model="openai/gpt-4o-mini",
            api_base=deployment_url,
            api_key=self.api_key,
            timeout=self.timeout,
        )

    @property
    def llm(self) -> ChatLiteLLM:
        """Returns a ChatLiteLLM instance configured to use DataRobot's LLM Gateway or a specific deployment."""
        if os.environ.get("LLM_DATAROBOT_DEPLOYMENT_ID"):
            return self.llm_with_datarobot_deployment
        else:
            return self.llm_with_datarobot_llm_gateway

    @staticmethod
    def make_system_prompt(suffix: str) -> str:
        return (
            "You are a helpful AI assistant, collaborating with other assistants."
            " Use the provided tools to progress towards answering the question."
            " If you are unable to fully answer, that's OK, another assistant with different tools "
            " will help where you left off. Execute what you can to make progress."
            f"\n{suffix}"
        )

    @property
    def agent_drive_searcher(self) -> CompiledGraph:
        return create_react_agent(
            self.llm,
            tools=[list_drive_files_tool(self.google_token)],
            prompt=self.make_system_prompt(
                """
You are a Google Drive assistant helping a user find relevant files in their Drive.
You have a tool that takes a space-separated list of words to search the name and body 
of the files for. Your job is to translate the user's question into 3-5 key words, 
use your tool to search for those key words (separated by spaces) and then return
the resulting list to the users.
""".strip()
            ),
        )

    def task_drive_search(self, state: MessagesState) -> Command[Any]:
        result = self.agent_drive_searcher.invoke(state)
        result["messages"][-1] = HumanMessage(
            content=result["messages"][-1].content, name="drive_node"
        )
        return Command(update={"messages": result["messages"]}, goto=END)

    def graph(self) -> CompiledStateGraph:
        workflow = StateGraph(MessagesState)
        workflow.add_node("drive_node", self.task_drive_search)
        workflow.add_edge(START, "drive_node")
        execution_graph = workflow.compile()
        return execution_graph

    def run(
        self, completion_create_params: CompletionCreateParams
    ) -> tuple[list[Any], dict[str, int]]:
        """Run the agent with the provided completion parameters.

        [THIS METHOD IS REQUIRED FOR THE AGENT TO WORK WITH DRUM SERVER]

        Inputs can be extracted from the completion_create_params in several ways. A helper function
        `create_inputs_from_completion_params` is provided to extract the inputs as json or a string
        from the 'user' portion of the input prompt. Alternatively you can extract and use one or
        more inputs or messages from the completion_create_params["messages"] field.

        Args:
            completion_create_params (CompletionCreateParams): The parameters for
                the completion request, which includes the input topic and other settings.
        Returns:
            tuple[list[Any], CrewOutput]: A tuple containing a list of messages (events) and the crew output.

        """
        # Check if streaming is requested from the completion params
        streaming = completion_create_params.get("stream", False)

        # Example helper for extracting inputs as a json from the completion_create_params["messages"]
        # field with the 'user' role: (e.g. {"topic": "Artificial Intelligence"})
        inputs = create_inputs_from_completion_params(completion_create_params)

        # If inputs are a string, convert to a dictionary with 'topic' key for this example.
        if isinstance(inputs, str):
            inputs = {"question": inputs}

        # Print commands may need flush=True to ensure they are displayed in real-time.
        print("Running agent with inputs:", inputs, flush=True)

        # Construct the input message for the langgraph graph.
        input_message = {
            "messages": [
                (
                    "user",
                    inputs["question"],
                )
            ],
        }

        # Graph stream is a generator that will execute the graph
        graph_stream = self.graph().stream(
            input_message,
            # Maximum number of steps to take in the graph
            {"recursion_limit": 150},
            debug=True,
        )

        if streaming:
            # For streaming, yield events as they happen
            def event_generator():
                events = []
                for event in graph_stream:
                    events.append(event)
                    yield event
            
            return event_generator()
        else:
            # For non-streaming, collect all events
            events = [event for event in graph_stream]
            return events
