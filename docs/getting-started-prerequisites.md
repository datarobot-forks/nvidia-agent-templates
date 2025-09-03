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

# Prerequisites

Before getting started, ensure you have the following tools installed on your system. You can use `brew` (on macOS) 
or your preferred package manager. Please ensure your local tools are at or above the minimum versions required.

| Tool | Version | Description | Installation guide |
|------|---------|-------------|-------------------|
| **uv** | >= 0.6.10 | A Python package manager. | [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) |
| **Pulumi** | >= 3.163.0 | An Infrastructure as Code tool. | [Pulumi installation guide](https://www.pulumi.com/docs/iac/download-install/) |
| **Taskfile** | >= 3.43.3 | A task runner. | [Taskfile installation guide](https://taskfile.dev/#/installation) |

More information about this stack is [here](docs/uv-task-pulumi.md).

## Installation instructions
The following sections provide common installation instructions for each tool, but please refer to the official
documentation links above for the most up-to-date instructions.

### UV
Installation on mac (using Homebrew):
```bash
brew install astral-sh/astral/uv
```

Installation on mac and linux:
```bash
curl -fsSL https://uv.astral.sh/install.sh | sh
```

Installation on Windows (using PowerShell):
```powershell
irm https://uv.astral.sh/install.ps1 | iex
```

### Pulumi
Installation on mac (using Homebrew):
```bash
brew install pulumi
```

Installation on mac and linux:
```bash
curl -fsSL https://get.pulumi.com/ | sh
```

Installation on Windows (using PowerShell):
```powershell
irm https://get.pulumi.com/windows.ps1 | iex
```

### Taskfile
Installation on mac (using Homebrew):
```bash
brew install go-task/tap/go-task
```

Installation on mac and linux:
```bash
curl -sL https://taskfile.dev/install.sh | sh
```

Installation on Windows (using Scoop):
```powershell
scoop install task
```
