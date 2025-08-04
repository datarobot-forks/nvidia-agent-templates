#!/bin/bash
if [ -z "$DATAROBOT_API_TOKEN" ]; then
    echo "Error: DATAROBOT_API_TOKEN environment variable is not set."
    exit 1
fi
if [ -z "$DATAROBOT_ENDPOINT" ]; then
    echo "Error: DATAROBOT_ENDPOINT environment variable is not set."
    exit 1
fi
if [ -z "$DATAROBOT_DEFAULT_EXECUTION_ENVIRONMENT" ]; then
    echo "DATAROBOT_DEFAULT_EXECUTION_ENVIRONMENT not set, environment will be built from docker_context."
fi

{
  echo "DATAROBOT_API_TOKEN=$DATAROBOT_API_TOKEN"; \
  echo "DATAROBOT_ENDPOINT=$DATAROBOT_ENDPOINT"; \
  echo "PULUMI_CONFIG_PASSPHRASE="; \
  echo "DATAROBOT_DEFAULT_USE_CASE="; \
  echo "USE_DATAROBOT_LLM_GATEWAY=true"; \
  echo "DATAROBOT_DEFAULT_EXECUTION_ENVIRONMENT=$DATAROBOT_DEFAULT_EXECUTION_ENVIRONMENT"; \
} >> .env

echo "Current environment variables:"
cat .env

# Source environment variables from .env file if it exists
if [ -f .env ]; then
    echo "Loading environment variables from .env file..."
    set -a  # automatically export all variables
    # shellcheck disable=SC1091
    source .env
    set +a  # turn off automatic export
else
    echo "Warning: .env file not found, continuing without environment variables"
fi

# Check if a number argument was provided
if [ $# -eq 0 ]; then
    echo ""
    echo "--------------------------------------------------"
    echo "Usage: $0 <agent_name>"
    echo "Example: $0 crewai, base, langgraph, llamaindex"
    exit 1
fi

# Get the number from the first argument
AGENT=$1

# Set the number based on the agent type
if [ "$AGENT" = "crewai" ]; then
    NUMBER="1"
elif [ "$AGENT" = "base" ]; then
    NUMBER="2"
elif [ "$AGENT" = "langgraph" ]; then
    NUMBER="3"
elif [ "$AGENT" = "llamaindex" ]; then
    NUMBER="4"
else
    # You can add other mappings here if needed
    NUMBER="0"
fi

echo "--------------------------------------------------"
echo "Running test for $AGENT agent"
echo "--------------------------------------------------"

echo "Running quickstart with selection: $AGENT (number: $NUMBER)"

# Run the quickstart command with the provided number
echo "START QUICKSTART"
echo "$NUMBER" | uv run quickstart.py
task setup
rm infra/infra/llm_datarobot.py

# Setup the local environment
echo "START TESTING"
cp .env api_tests/.env
cd api_tests || exit 1
uv run pytest -vv -s -k "test_e2e_agent_$AGENT" --ignore-glob=**e2e_test_dir*
