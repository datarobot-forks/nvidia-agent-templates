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

> **NOTE:** Please ensure all prerequisites are installed before proceeding with getting started.

### Step 1: Clone the Repository

```bash
git clone https://github.com/datarobot-community/datarobot-agent-templates.git
cd datarobot-agent-templates
```

Alternatively, you can download the repository as a ZIP file and extract it to your preferred location.

### Step 2: Configure Environment Variables

Create a `.env` file in the root directory to store your configuration:

```bash
# Copy the sample environment file
cp .env.sample .env

# Edit the file with your preferred editor
nano .env  # or vim .env, code .env, etc.
```

Your `.env` file must contain the minimum following variables:

```bash
# DataRobot API keys and endpoint
DATAROBOT_API_TOKEN=<Your API Token>
DATAROBOT_ENDPOINT=https://app.datarobot.com/api/v2
```

### Step 3: Decide On Your Agent Framework

This repository includes four templates to get started, these are selected during the quickstart process:

| Directory | Framework | Description |
|-----------|-----------|-------------|
| `agent_crewai` | CrewAI | Role-based multi-agent collaboration framework |
| `agent_langgraph` | LangGraph | State-based orchestration framework |
| `agent_llamaindex` | Llama-Index | RAG-focused framework |
| `agent_generic_base` | Generic | Base template for any framework |

### Step 4: Use Quickstart To Get Started

A `quickstart.py` and a `task start` command are provided to help you quickly setup your environment and
remove all unnecessary files. You can run the quickstart script to initialize your agent:

```bash
python quickstart.py
# python3 quickstart.py  # If python points to Python 2.x
# uv run quickstart.py  # If using uv
```
or use the Taskfile command:

```bash
task start
```

Answer the prompts to select your agent framework and configure the initial setup. This will remove any
unused files from the repo and prepare help you prepare your environments for agent development and testing.

## Developing Your Agent

Developing your agent is straightforward and a variety of tools and commands are provided to help you. Please
see the documentation for your chosen framework for specific development guidelines.

<span style="font-size:1.5em;">[Agent Development Documentation](./agent_generic_base/README.md)</span>

## Getting Help

If you encounter issues or have questions, please:

- Check the documentation for your chosen framework
- Visit the [DataRobot Community](https://community.datarobot.com/) for support
- Open an issue on the [GitHub repository](https://github.com/datarobot-community/datarobot-agent-templates)
