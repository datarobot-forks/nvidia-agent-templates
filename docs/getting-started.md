### DataRobot Agent Templates Navigation
- [Home](/README.md)
- [Prerequisites](/docs/getting-started-prerequisites.md)
- [Getting started](/docs/getting-started.md)
- Developing Agents
  - [Developing your agent](/docs/developing-agents.md)
  - [Using the agent CLI](/docs/developing-agents-cli.md)
  - [Adding python requirements](/docs/developing-agents-python-requirements.md)
  - [Configuring LLM providers](/docs/developing-agents-llm-providers.md)
---

# Getting started

> **NOTE:** Please ensure all [prerequisites](/docs/getting-started-prerequisites.md) are installed before proceeding with the following workflow.

### Step 1: Clone the repository

Clone the repository to your local machine using Git or you can download it as a ZIP file.

```bash
git clone https://github.com/datarobot-community/datarobot-agent-templates.git
cd datarobot-agent-templates
```

For on-premise users, please ensure you clone the correct branch for your release
(e.g. `git clone -b release/11.1 https://github.com/datarobot-community/datarobot-agent-templates.git`).

### Step 2: Configure environment variables

Create an `.env` file in the root directory to store your configuration. This must be done before running any
additional commands.

```bash
# Copy the sample environment file
cp .env.sample .env

# Edit the file with your preferred editor
nano .env  # or vim .env, code .env, etc.
```

Your `.env` file must contain, at minimum, the following variables, but it is recommended to set all variables for a
complete setup. We recommend leaving all other variables at their default values during the getting started process.

```bash
# DataRobot API keys and endpoint
DATAROBOT_API_TOKEN=<Your API Token>
DATAROBOT_ENDPOINT=https://app.datarobot.com/api/v2
```

**For cloud users you should use the above endpoint. For on-premise users, please use the appropriate endpoint for your
environment.**

### Step 3: Choose an agent framework

This repository includes four templates to get started. They are selected during the quickstart process.

| Directory | Framework | Description |
|-----------|-----------|-------------|
| `agent_crewai` | CrewAI | Role-based multi-agent collaboration framework |
| `agent_langgraph` | LangGraph | State-based orchestration framework |
| `agent_llamaindex` | Llama-Index | RAG-focused framework |
| `agent_generic_base` | Generic | Base template for any framework |

### Step 4: Start

The templates provide a helper script to start the development process. Just run

```bash
task start
```

Answer the prompts to select your agent framework and configure the initial setup. This will remove any
unused files from the repository and help you prepare your environments for agent development and testing.

After running `task start` you can run `task` from the root directory to see available commands.

> **IMPORTANT:** Before continuing to the next step, please ensure that you have run `task install`, as prompted
> during the quickstart, to install and set up the agent and infrastructure environments.

### Step 5: Test your agent is working locally
You can use the CLI to test your agent locally. Run the following command from the root directory:

```bash
task agent:cli -- execute --user_prompt 'Tell me about Generative AI'
```

### Step 6: Deploy your agent to DataRobot
When you are ready to deploy your agent to DataRobot, run the following command from the root directory:
```bash
task deploy
```

You will need to provide a **pulumi stack name** but this is only required the first time you deploy and is
used for tracking your deployment. You can use any name you like, for example `test`, `dev` or `production`.

### Step 7: Test your deployed agent
You can use the CLI to test your deployed agent. You will need the deployment ID which is shown after the
deployment process is complete. You can find the deployment ID in the terminal. You can also find the deployment
ID in the DataRobot UI under the "Deployments" section under "Console".

```bash
task agent:cli -- execute-deployment --deployment_id %your_id% --user_prompt 'Tell me about Generative AI'
```

### Step 8: Develop your agent
You are now ready to start developing your agent! Please refer to the
[Developing Agents](/docs/developing-agents.md) documentation for the next steps on:
  - [Developing your agent](/docs/developing-agents.md)
  - [Using the agent CLI](/docs/developing-agents-cli.md)
  - [Adding python requirements](/docs/developing-agents-python-requirements.md)
  - [Configuring LLM providers](/docs/developing-agents-llm-providers.md)


