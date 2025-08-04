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

# Install Pulumi
RUN curl -fsSL https://get.pulumi.com | sh
ENV PATH="/root/.pulumi/bin:${PATH}"

# Verify installations
RUN uv --version && \
    task --version && \
    pulumi version

# Copy all files from parent directory into workspace
COPY . /workspace
COPY ./api_tests/docker_context/setup.sh /workspace/setup.sh
RUN chmod +x /workspace/setup.sh

# Set working directory
WORKDIR /workspace

# Default command
ENTRYPOINT ["/workspace/setup.sh"]
