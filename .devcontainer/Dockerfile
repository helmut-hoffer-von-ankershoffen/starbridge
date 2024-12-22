FROM mcr.microsoft.com/devcontainers/python:0-3.11-bullseye

# Install system dependencies
RUN apk add \
    curl \
    jq \
    libxml2-utils \
    gnupg2 \
    libcairo2 \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN apk add nodejs npm \
    && rm -rf /var/lib/apt/lists/*

# Install MCP Inspector
RUN npm install @modelcontextprotocol/inspector@0.3.0
