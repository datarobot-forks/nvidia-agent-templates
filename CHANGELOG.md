# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

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
