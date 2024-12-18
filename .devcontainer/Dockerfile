FROM mcr.microsoft.com/devcontainers/python:0-3.11-bullseye

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    jq \
    libxml2-utils \
    libcairo2 \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*
