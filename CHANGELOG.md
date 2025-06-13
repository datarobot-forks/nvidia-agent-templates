# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## 0.1.2
- Add ability to send chat completion to CLI as complete json file
- A default environment is now provided in the `.env.sample` and building from context is now optional, not required
- Ignore temporary or build files when creating the `custom_model`
- Renamed pulumi variables to be more concise and uniform
- Remove deprecated clientId parameter everywhere from chat endpoints
- Make DRUM server port retrieval dynamic
- Switched target for dev server to `agenticworkflow`
- Unpin chainguard base image to allow for latest updates
- Ensure Llamaindex has a `GPT` model or tools don't work
- Bump requests to fix the CVE

## 0.1.1
- Add support for `AgenticWorkflow` agent target type
- Remove unused runtime parameter
- Re-introduce moderation library
- Add stdout log handling in ipykernel environments
- Use UV override for correct LiteLLM version
- Add end-to-end tests for agent execution
- Fixes to tools
- Address jupyter-core CVE
- Support tracing
- Improvements and fixes to environments
- Documentation improvements

## 0.1.0
- Changes to `run_agent.py`
- Improve component testing
- Add basic support for moderations helpers for agents
- Ensure all taskfile commands are properly inherited from the `taskfile` template
- Add descriptions and inheritance to all taskfile commands
- Add quickstart functionality to the repository
- Upgrade LiteLLM
- Add datarobot-moderations package to requirements
- Bump `datarobot-pulumi-utils`
- Add `pyproject.toml` to the root to assist with quickstart and development
- Allow agents to receive string or json gracefully
- Ensure that environment variables are properly passed to LiteLLM with helper functions

## 0.0.6
- Documentation and getting started rewritten and improved.
- Add Taskfile improvements for development.
- Support `requirements.txt` integration in `custom_model` folder.
- Add `build` and `deploy` commands to the `taskfile` for `pulumi` integration.
- Add feature flag verification during `pulumi` operations.
- Allow dynamically passing model name to agents.
- Pin ipykernel to resolve issues.
- Bump requirements to resolve CVEs.
- Improve repository test coverage and refine execution testing scripts.

## 0.0.5
- Finalize support for open telemetry to all frameworks.
- Update execution environments to resolve CVEs.
- Revert target types to `textgeneration` to resolve deployment issues.

## 0.0.4
- Add initial support for open telemetry.

## 0.0.3
- Bug fixes
- Allow sending OpenAI complete dictionary to run_agent.
- Add support for integrating agent tooling.

## 0.0.2
- Add support for `LlamaIndex` agents.

## 0.0.1
- Add `af-component-agent` template to the repository.
- Update the `agent_crewai` agent with a simple flow.
- Added `agent_cli` and `taskfile` to the `agent_crewai` agent.
- Add support for `CrewAI` agents.
- Add support for `Langgraph` agents.
- Complete development of `run_agent.py` concept.
