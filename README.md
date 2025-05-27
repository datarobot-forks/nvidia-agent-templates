# [DataRobot AI Agent Templates](https://github.com/datarobot-community/datarobot-agent-templates)

This repository provides ready-to-use templates for building and deploying AI agents with multi-agent frameworks. These templates streamline the process of setting up your own agents with minimal configuration requirements. They support:

- Local development workflows
- Remote development (via GitHub Codespaces)
- Building and deploying agents within DataRobot

## Prerequisites

Before getting started, ensure you have the following tools installed on your system. You can use `brew` (on macOS) or your preferred package manager:

| Tool | Description | Installation Guide |
|------|-------------|-------------------|
| **uv** | Python package manager | [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) |
| **Pulumi** | Infrastructure as Code tool | [Pulumi installation guide](https://www.pulumi.com/docs/iac/download-install/) |
| **Taskfile** | Task runner | [Taskfile installation guide](https://taskfile.dev/#/installation) |

## Available Templates

This repository includes templates for four popular agent frameworks:

| Framework | Description | GitHub Repository |
|-----------|-------------|-------------------|
| **CrewAI** | Multi-agent framework with focus on role-based agents | [GitHub](https://github.com/crewAIInc/crewAI) |
| **LangGraph** | Multi-agent orchestration with state graphs | [GitHub](https://github.com/langchain-ai/langgraph) |
| **Llama-Index** | Framework for building RAG systems | [GitHub](https://github.com/run-llama/llama_index) |
| **Generic Base** | Flexible template for any custom framework | - |

## Getting Started

### Step 1: Clone the Repository

```bash
git clone https://github.com/datarobot-community/datarobot-agent-templates.git
cd datarobot-agent-templates
```

Alternatively, you can download the repository as a ZIP file and extract it to your preferred location.

### Step 2: Choose Your Agent Framework

This repository includes four template directories, one for each supported framework:

| Directory | Framework | Description |
|-----------|-----------|-------------|
| `agent_crewai/` | CrewAI | Role-based multi-agent collaboration framework |
| `agent_langgraph/` | LangGraph | State-based orchestration framework |
| `agent_llamaindex/` | Llama-Index | RAG-focused framework |
| `agent_generic_base/` | Generic | Base template for any framework |

> **Note:** You only need to keep the template directory for your chosen framework. You can safely delete the other template directories to simplify your workspace.

### Step 3: Review the Infrastructure Templates

The `infra/infra/` directory contains Pulumi templates for deploying your agent:

| Template File | Purpose |
|---------------|---------|
| `agent_crewai.py` | Pulumi deployment for CrewAI agents |
| `agent_langgraph.py` | Pulumi deployment for LangGraph agents |
| `agent_llamaindex.py` | Pulumi deployment for Llama-Index agents |
| `agent_generic_base.py` | Pulumi deployment for generic agents |
| `llm_datarobot.py` | Pulumi template for LLM deployments (compatible with all agents) |

> **Note:** You should keep only the infrastructure template corresponding to your chosen agent framework, plus the `llm_datarobot.py` file if you plan to use DataRobot as your LLM backend.

## Setting Up Your Development Environment

### Step 1: Configure Environment Variables

Create a `.env` file in the root directory to store your configuration:

```bash
# Copy the sample environment file
cp .env.sample .env

# Edit the file with your preferred editor
nano .env  # or vim .env, code .env, etc.
```

Your `.env` file should contain the following variables:

```bash
# DataRobot API keys and endpoint
DATAROBOT_API_TOKEN=<Your API Token>
DATAROBOT_ENDPOINT=https://app.datarobot.com/api/v2

# Required, unless logged in to pulumi cloud
PULUMI_CONFIG_PASSPHRASE=

# If empty, a new use case will be created
DATAROBOT_DEFAULT_USE_CASE=

# If empty, a new execution environment will be created
DATAROBOT_DEFAULT_EXECUTION_ENVIRONMENT=
```

### Step 2: Navigate to Your Agent Directory

Change to the directory for your chosen agent framework:

```bash
cd agent_crewai  # or agent_langgraph, agent_llamaindex, agent_generic_base
```

### Step 3: Set Up the Agent Environment

Install dependencies and set up the local environment:

```bash
task req
```

This command will create a virtual environment (`.venv`) and install all required dependencies using `uv`.

## Developing Your Agent

### Available Task Commands

The repository uses Taskfile to simplify common operations. View available commands by running:

```bash
task
```

This will display a list of available commands:

```
Available task commands:
  To run commands, use the following format:
    task <command> [<args>]

Commands:
help                           - Show this help message
req                            - Update dependencies for the agent
cli                            - Run the CLI with the provided arguments
lint                           - Lint the agent templates
test                           - Run unit tests for the agent
fix-licenses                   - Fix licenses for the agent files
```

### Using the Agent CLI

The `task cli` command provides a convenient interface for testing your agent:

```bash
task cli
```

This will display CLI usage information:

```
Running CLI
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

  A CLI for interacting executing agent custom models using the chat endpoint
  and OpenAI completions.

Options:
  --codespace_id TEXT  Codespace ID for the session.
  --api_token TEXT     API token for authentication.
  --base_url TEXT      Base URL for the API.
  --help               Show this message and exit.

Commands:
  execute             Execute agent code using OpenAI completions.
  execute-deployment  Query a deployed model using the command line.
```

### Modifying the Agent Code

The main agent code is located in the `custom_model` directory:

| File | Purpose |
|------|---------|
| `agent.py` | The main agent implementation file |
| `custom.py` | Handles execution of the agent in DataRobot |
| `helpers.py` | Helper functions for the agent |
| `tools_client.py` | Tool definitions for the agent |

The main class you'll need to modify is in `agent.py`. The standard implementation pattern is:

```python
class MyAgent:
    def __init__(
        self, api_key: str, api_base: str, verbose: Union[bool, str], **kwargs: Any
    ):
        self.api_key = api_key
        self.api_base = api_base
        if isinstance(verbose, str):
            self.verbose = verbose.lower() == "true"
        elif isinstance(verbose, bool):
            self.verbose = verbose

    def run(self, inputs: Dict[str, str]) -> Tuple[str, Dict[str, int]]:
        _ = inputs, self.api_key
        usage = {
            "completion_tokens": 0,
            "prompt_tokens": 0,
            "total_tokens": 0,
        }
        return "success", usage
```

> **Note:** If you rename the `MyAgent` class, you'll need to update the reference in `custom.py`.

## Testing Your Agent

There are two primary methods for testing your agent:

### Method 1: Using the CLI (Recommended)

Test your agent using the CLI interface with a sample prompt:

```bash
task cli -- execute --user_prompt '{"topic": "Artificial Intelligence"}'
```

The JSON object is passed directly to your agent's `run` method as the `inputs` parameter.

### Method 2: Using Direct Execution

For more advanced testing scenarios, you can use the `run_agent.py` script directly:

```bash
uv run run_agent.py --chat_completion '{"your": "parameters"}' --custom_model_dir "./custom_model"
```

## Building and Deploying Your Agent

When you're ready to move your agent to DataRobot, you have two options depending on your needs:

### Step 1: Ensure Environment Variables Are Set

Make sure your `.env` file contains the required DataRobot credentials and configuration:

```bash
DATAROBOT_API_TOKEN=<Your API Token>
DATAROBOT_ENDPOINT=https://app.datarobot.com/api/v2
PULUMI_CONFIG_PASSPHRASE=<Optional passphrase>
```

### Step 2: Choose Your Deployment Option

#### Option A: Build a Custom Model for Testing and Refinement

To create a custom model that can be refined using the DataRobot LLM Playground:

```bash
task build
```

This command runs the Pulumi infrastructure to create a custom model in DataRobot but does not create a full production deployment. This is significantly faster and is ideal for iterative development and testing.

#### Option B: Deploy to Production

To create a full production-grade deployment:

```bash
task deploy
```

This command builds the custom model and creates a production deployment with the necessary infrastructure, which takes longer but provides a complete production environment.

### Step 3: Manual Deployment (Alternative)

If needed, you can manually run the Pulumi commands:

```bash
# Load environment variables
set -o allexport && source .env

# For build mode only (custom model without deployment)
export DEPLOY=0

# Or for full deployment mode (default)
# export DEPLOY=1

# Navigate to the infrastructure directory
cd ./infra

# Run Pulumi deployment
pulumi up
```

The `DEPLOY` environment variable controls whether Pulumi creates only the custom model (`DEPLOY=0`) or both the custom model and a production deployment (`DEPLOY=1`). If not set, Pulumi defaults to full deployment mode.

Pulumi will prompt you to confirm the resources to be created or updated.

## Next Steps

After deployment, your agent will be available in your DataRobot environment. You can:

1. Test your deployed agent using `task cli -- execute-deployment`
2. Integrate your agent with other DataRobot services
3. Monitor usage and performance in the DataRobot dashboard

## Getting Help

If you encounter issues or have questions, please:

- Check the documentation for your chosen framework
- Visit the [DataRobot Community](https://community.datarobot.com/) for support
- Open an issue on the [GitHub repository](https://github.com/datarobot-community/datarobot-agent-templates)
