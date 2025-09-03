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

# Developing Agents

Developing an agent is straightforward and a variety of tools and commands are provided to help you. [See the documentation for your chosen framework](./agent_generic_base/README.md) for development-specific guidelines.

## Modify the agent code

The first step in developing your agent is to modify the agent code to implement your desired functionality.
The main agent code is located in the `custom_model` directory inside the framework-specific directory you selected when
you created the project. For example, if you selected the CrewAI framework, the path would be `agent_crewai/custom_model`.

| File | Purpose |
|------|---------|
| `agent.py` | The main agent implementation file. |
| `custom.py` | Handles execution of the agent in DataRobot. |
| `helpers.py` | Helper functions for the agent. |
| `tools_client.py` | Tool definitions for the agent. |

The main class you need to modify is in `agent.py`. See this class for details of the implementation
based on the framework for which you are developing.

The agent template provides you with a simple example that contains 3 agents and 3 tasks. You can modify this code
to add more agents, tasks, and tools as needed.  Each agent is connected to an LLM provider, which is specified by 
the `def llm` function in the `agent.py` file. You can modify this function to change the LLM provider or its 
configuration. See the [Configuring LLM providers](docs/developing-agents-llm-providers.md) documentation for more 
details.

## Build and deploy an agent

When you're ready to move your agent to DataRobot, you have two options depending on your needs.

### Step 1: Ensure that the environment variables are set

Make sure your `.env` file contains the required DataRobot credentials and configuration:

```bash
DATAROBOT_API_TOKEN=<Your API Token>
DATAROBOT_ENDPOINT=https://app.datarobot.com/api/v2
PULUMI_CONFIG_PASSPHRASE=<Optional passphrase>
```

### Choose your deployment option

#### Option A: Build a custom model for testing and refinement

To create a custom model that can be refined using the DataRobot LLM Playground.

```bash
task build
```

This command runs the Pulumi infrastructure to create a custom model in DataRobot but does not create a full production deployment. This is significantly faster and is ideal for iterative development and testing.

#### Option B: Deploy to production

To create a full production-grade deployment:

```bash
task deploy
```

This command builds the custom model and creates a production deployment with the necessary infrastructure, which takes longer but provides a complete production environment.

### Step 3: Manual deployment (Alternative)

If needed, you can manually run the Pulumi commands.

```bash
# Load environment variables
set -o allexport && source .env

# For build mode only (custom model without deployment)
export AGENT_DEPLOY=0

# Or for full deployment mode (default)
# export AGENT_DEPLOY=1

# Navigate to the infrastructure directory
cd ./infra

# Run Pulumi deployment
pulumi up
```

The `AGENT_DEPLOY` environment variable controls whether Pulumi creates only the custom model (`DEPLOY=0`) or both the custom model and a production deployment (`DEPLOY=1`). If not set, Pulumi defaults to full deployment mode.

Pulumi will prompt you to confirm the resources to be created or updated.

## Next steps

After deployment, your agent will be available in your DataRobot environment. You can:

1. Test your deployed agent using `task cli -- execute-deployment`.
2. Integrate your agent with other DataRobot services.
3. Monitor usage and performance in the DataRobot dashboard.