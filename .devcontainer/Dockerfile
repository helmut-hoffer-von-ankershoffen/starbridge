FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

RUN apt update -y && \
    apt install -y --no-install-recommends curl gnupg2 jq less libcairo2 nano procps psmisc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
