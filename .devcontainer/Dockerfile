FROM mcr.microsoft.com/devcontainers/python:0-3.11-bullseye

# Install system dependencies
RUN apk add \
    curl \
    jq \
    libxml2-utils \
    libcairo2 \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN apk add nodejs npm

