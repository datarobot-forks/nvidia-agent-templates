# Introduction

This repository contains an example application template for building an agentic
application on the DataRobot platform with OAuth integration built on top of the
Langgraph agentic framework. When deployed, this template sets up

1. A DataRobot agentic custom model leveraging LangGraph.
2. A DataRobot application with a FastAPI backend and React frontend for
   chatting with the agent.

This simple example demonstrates a single agent with a search tool for Google Drive
which can assist users in searching for relevant files in their Drive folder. In order
to authorize the agent to search Drive on behalf of their user, the application implements
an OAuth authorization server, providing a hook for the user to authorize the app to read
their Google Drive.

# Getting Started

## Quick Start

### Prerequisites

If you are using DataRobot Codespaces, this is already complete for you. If not, install the following tools:

- [Taskfile.dev](https://taskfile.dev/#/installation) (task runner)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (Python package manager)
- [Pulumi](https://www.pulumi.com/docs/iac/download-install/) (infrastructure as code)

#### Example Installation Commands

For the latest and most accurate installation instructions for your platform, visit:
* https://taskfile.dev/installation/
* https://www.pulumi.com/docs/iac/download-install/
* https://docs.astral.sh/uv/getting-started/installation/

We provide the instructions below to save you a context flip, but your system may not meet the common expectations from these shortcut scripts:

**macOS:**
```sh
brew install go-task/tap/go-task
brew install uv
brew install pulumi/tap/pulumi
```

**Linux (Debian/Ubuntu/DataRobot Codespaces):**
```sh
# Taskfile.dev
sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b ~/.local/bin
# uv
curl -Ls https://astral.sh/uv/install.sh | sh
# Pulumi
curl -fsSL https://get.pulumi.com | sh
```

**Windows (PowerShell):**
```powershell
# Taskfile.dev
winget install --id=GoTask.GoTask -e
# uv
winget install --id=astral-sh.uv  -e
# Pulumi
winget install pulumi
winget upgrade pulumi
```

### Pulumi Login

Pulumi requires a location to store the state of the application template. The easiest option is to
run:

```
pulumi login --local
```

We recommend using a shared backend like Ceph, Minio, S3, or Azure Blob Storage. See
[Managing Pulumi State and Backends](https://www.pulumi.com/docs/iac/concepts/state-and-backends/) for
more details. For production CI/CD information see our comprehensive
[CI/CD Guide for Application Templates](https://docs.datarobot.com/en/docs/workbench/wb-apps/app-templates/pulumi-tasks/cicd-tutorial.html)

### Clone the Repository

```sh
git clone https://github.com/datarobot-community/talk-to-my-docs-agents
cd talk-to-my-docs-agents
```

### Environment Setup

Copy the sample environment file and fill in your credentials:

```sh
cp .env.sample .env
# Edit .env with your API keys and secrets
```

The `task` commands will automatically read the `.env` file directly to ensure each task gets the correct configuration.
If you need to source those variables directly into your shell you can:

**Linux/macOS:**
```sh
set -a && source .env && set +a
```

**Windows (PowerShell):**
```powershell
Get-Content .env | ForEach-Object {
	if ($_ -match '^\s*([^#][^=]*)=(.*)$') {
		[System.Environment]::SetEnvironmentVariable($matches[1], $matches[2])
	}
}
```

### Initial Configuration

The `.env.template` file contains the relevant configuration values needed by the app.

You will need a DataRobot API token for a user. You can generate one at the
`account/developer-tools` endpoint for your DataRobot stack, e.g.
https://app.datarobot.com/account/developer-tools. From that page you can grab
and fill in.

```
DATAROBOT_API_TOKEN=
DATAROBOT_ENDPOINT=
```

You will also need to configure your Google client ID and secret. See the following section.

#### Google OAuth Application

- Go to [Google API Console](https://console.developers.google.com/) from your Google account
- Navigate to "APIs & Services" > "Enabled APIs & services" > "Enable APIs and services" search for Drive, and add it.
- Navigate to "APIs & Services" > "OAuth consent screen" and make sure you have your consent screen configured. You may have both "External" and "Internal" audience types.
- Navigate to "APIs & Services" > "Credentials" and click on the "Create Credentials" button. Select "OAuth client ID".
- Select "Web application" as Application type, fill in "Name" & "Authorized redirect URIs" fields. For example, for local development, the redirect URL will be:
  - `http://localhost:5173/oauth/callback` - local vite dev server (used by frontend folks)
  - `http://localhost:8080/oauth/callback` - web-proxied frontend 
  - `http://localhost:8080/api/v1/oauth/callback/` - the local web API (optional).
  -  For production, you'll want to add your DataRobot callback URL. For example, in US Prod it is `https://app.datarobot.com/custom_applications/{appId}/oauth/callback`. For any installation of DataRobot it is `https://<datarobot-endpoint>/custom_applications/{appId}/oauth/callback`.
- Hit the "Create" button when you are done.
- Copy the "Client ID" and "Client Secret" values from the created OAuth client ID and set them in the template env variables as `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` correspondingly.
- Make sure you have the "Google Drive API" enabled in the "APIs & Services" > "Library" section. Otherwise, you will get 403 errors.
- Finally, go to "APIs & Services" > "OAuth consent screen" > "Data Access" and make sure you have the following scopes selected:
  - `openid`
  - `https://www.googleapis.com/auth/userinfo.email`
  - `https://www.googleapis.com/auth/userinfo.profile`
  - `https://www.googleapis.com/auth/drive.readonly`

## Dev Flow

In order to create the necessary DataRobot infrastructure, we will send an initial deployment.

```
task install # install dependencies locally
task deploy
```

That `task deploy` will bundle local source and deploy the corresponding custom model and application
on DataRobot. This can be repeated to deploy the working application to DataRobot. To iterate locally,
use the `dev` task, which starts a local agent server, vite frontend and uvicorn backend which
watch for iteration.

```
task dev
```

As an application progresses from POV to production, you will want to invest in CI/CD.

## Production Considerations

To simplify development, this application persists its state in a SQLite file hosted on
DataRobot. This is not suitable beyond initial experimentation and should be replaced with
an external SQL database for production.

# Auth Flow

All DataRobot applications require DataRobot authentication and authorization: the accessor
must possess a identity with whom the application has been shared. See 
[this documentation for app sharing](https://docs.datarobot.com/en/docs/workbench/wb-apps/custom-apps/nxt-manage-custom-app.html#share-applications). 
This authentication and authorization is handled in a proxy before a request lands on the application;
this proxy identifies the user in the `X-USER-EMAIL` and (for DR platform users) `X-DATAROBOT-API-KEY`.
(See `web/auth/ctx.py:get_datarobot_ctx`).

The FastAPI backend implements methods for OAuth authorization code flow to an external provider like
Google (`web/app/api/v1/auth.py`). The `POST /chat` endpoint of the application (`web/app/api/v1/chat.py`)
has an example of retrieving the user's Google token and passing that in the extra body to our agentic 
custom model for use in a Drive tool.