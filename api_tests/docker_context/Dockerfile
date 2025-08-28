FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Update package list and install necessary dependencies
# hadolint ignore=DL3008
RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    wget \
    ca-certificates \
    git \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install go-task
RUN sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin

# Install Pulumi to a global location
RUN curl -fsSL https://get.pulumi.com | sh && \
    mv /root/.pulumi/bin/* /usr/local/bin/ && \
    rm -rf /root/.pulumi

# Verify installations
RUN uv --version && \
    task --version && \
    pulumi version

# Create a non-root user with home directory
RUN groupadd -r appuser && useradd -r -g appuser -m -d /home/appuser appuser

# Copy files and set permissions
COPY . /workspace
COPY ./api_tests/docker_context/setup.sh /workspace/setup.sh
RUN chmod +x /workspace/setup.sh \
    && chown -R appuser:appuser /workspace /home/appuser

# Precache uv plugins for faster test runs
WORKDIR /workspace/agent_crewai
RUN task install
WORKDIR /workspace/agent_generic_base
RUN task install
WORKDIR /workspace/agent_langgraph
RUN task install
WORKDIR /workspace/agent_llamaindex
RUN task install

# Set working directory
WORKDIR /workspace

# Switch to non-root user
USER appuser

# Default command
ENTRYPOINT ["/workspace/setup.sh"]
