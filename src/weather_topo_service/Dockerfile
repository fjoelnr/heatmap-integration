# Stage 1: Build
FROM --platform=$BUILDPLATFORM python:3.9-slim AS builder

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt /app/
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

# Copy the rest of the application
COPY . /app/

# Set entrypoint and command
ENTRYPOINT ["python3"]
CMD ["app.py"]

# Stage 2: Development Environment
FROM builder AS dev-envs

# Install additional packages for development
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Create a new user and group
RUN groupadd -r docker && \
    useradd -r -s /bin/bash -g docker vscode

# Install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /
