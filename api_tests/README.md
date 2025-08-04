# DataRobot AI agent templates API Acceptance Tests

This test suite is designed to validate a simulated local execution environment along with API connectivity to
DataRobot. It ensures that the agent templates can be built, deployed, and executed correctly within DataRobot's
infrastructure and that the templates and backend services are functioning as expected.


## Prerequisites

Please ensure your local tools are at or above the minimum versions required. These tests utilize docker to run the 
agent templates in a simulated environment, and they require several tools to be installed on your system.

| Tool         | Version | Description | Installation guide                                                               |
|--------------|---------|-------------|----------------------------------------------------------------------------------|
| **uv**       | >= 0.6.10 | A Python package manager. | [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) |
| **Pulumi**   | >= 3.163.0 | An Infrastructure as Code tool. | [Pulumi installation guide](https://www.pulumi.com/docs/iac/download-install/)   |
| **Taskfile** | >= 3.43.3 | A task runner. | [Taskfile installation guide](https://taskfile.dev/#/installation)               |
| **Docker**   | >= 28.0.4 | A task runner. | [Docker installation guide](https://docs.docker.com/engine/install/)                 |

## Setup

Authentication to DataRobot is required to run these tests. Please copy or rename `.env.example` to `.env` and
fill in the required fields with your DataRobot credentials. This file is used to configure the environment variables.
By providing additional fields, the API tests will simulate running using that specific environment configuration.

> The API Tests .env file is only a subset of the DataRobot AI Agent Templates .env file. Some variables and settings
> are hardcoded in the API tests and are not configurable through the .env file because they are not relevant to the 
> API tests.

## Running the Tests

You can use taskfile locally to execute the tests. The taskfile provides a convenient way to run the tests and manage
the environment. You can run the tests using the following command:

```bash
task test
```

Alternatively you can test a specific agent template by running:

```bash
task test-<template_name>  # (e.g. task test-base)
```

Tests can also be executed using a `harness` pipeline with the appropriate environment variables configured. Pipeline
templates are provided in the `harness` directory.

## Test Structure
The API tests for this repository need to test a mixture of local development and DataRobot API functionality. The
tests are therefore structured across 3 pieces of code:
1. `docker_context/Dockerfile`: This Dockerfile is used to build the simulated local development environment in a 
reproducible manner. This starts with a basic uv container and ensures that `uv`, `taskfile` and `pulumi` are all
installed into the basic container. It also copies the files, simulating a `git clone` action. The docker container
itself does not run any tests during the build stage.
2. `docker_context/setup.sh`: This script is used to initiate the tests and perform some basic user actions upfront.
    - It creates a basic `.env` file with the required DataRobot credentials from the host environment.
    - It selects an agent template with quickstart.
    - It will initialize the uv environments and install the required dependencies.
    - It removes files not required for a "happy path" test run.
    - It triggers the `uv run pytest` command to run the tests.
3. `api_tests/`: This directory contains the actual tests that are run by pytest. The tests are designed to validate
that the agent templates can be built, deployed, and executed correctly within DataRobot's infrastructure.
   - The tests are structured to cover various aspects of the agent templates, including API connectivity, template
   functionality, and backend service interactions.
   - The tests are written in Python and utilize the pytest framework for execution.
   - The tests perform the following actions:
     - Initialize the pulumi environment using the appropriate environment variables.
     - Test the agent local execution and development environment and that the agent runs and responds.
     - Test the `task build` functionality via `pulumi`.
     - Connect to the custom model via the `DataRobot Playground API` and validate the agent runs and responds.
     - Test the `task deploy` functionality via `pulumi`.
     - Connect to the deployment the `MMM Deployment API` and validate the agent runs and responds.
     - Teardown the pulumi environment to clean up resources whether success or failure.
4. `Taskfile.yml` This file is used to define the tasks that can be run using the `task` command. It includes tasks for
   running the tests, building the docker images, and maintaining the code within the `api_tests`.
