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

# LLM Providers
One of the key components of an LLM agent is the underlying LLM provider. The template supports connecting to
any type of LLM provider. Within the DataRobot ecosystem, you can use either the DataRobot LLM Gateway or a custom
DataRobot deployment (this includes NIM deployments). Additionally you can connect to any external LLM provider that
supports the OpenAI API standard.

## Using a DataRobot Deployment as an LLM
_This method can also be used to dynamically pass any variable between pulumi deployments. The dependencies will
automatically be deployed in the appropriate order without any user input._

The template provides two LLM endpoints for the agent. The default method uses the DataRobot LLM Gateway. Alternatively,
you may use a custom deployment: either let pulumi create it for you, or use an existing one.

A sample Playground Model is provided in the `infra/infra/llm_datarobot.py` pulumi file.

1. Edit your `.env` file:
   ```bash
   USE_DATAROBOT_LLM_GATEWAY=false
   ```
2. If you wish to use an existing LLM deployment, set in `.env`:
   ```bash
   LLM_DATAROBOT_DEPLOYMENT_ID=<your_deployment_id>
   ```