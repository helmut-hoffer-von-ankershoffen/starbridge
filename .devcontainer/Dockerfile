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
RUN apk add nodejs npm

