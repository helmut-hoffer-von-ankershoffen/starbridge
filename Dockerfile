# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

RUN apt update -y && \
    apt install -y --no-install-recommends libcairo2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt update -y && \
    curl --proto '=https' --tlsv1.2 -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y --no-install-recommends nodejs npm && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt update -y && \
    apt install -y --no-install-recommends curl gnupg2 iputils-ping jq less libxml2-utils nano procps psmisc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN npm install --ignore-scripts -g @modelcontextprotocol/inspector@0.3.0

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --all-extras --no-dev --no-editable

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY pyproject.toml /app
COPY .python-version /app
COPY uv.lock /app
COPY src /app/src
COPY LICENSE /app
COPY *.md /app

COPY .env.example /app/.env.example
COPY tests /app/tests

# Install project specifics
# Nothing yet

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --all-extras --no-dev --no-editable

ENV STARBRIDGE_RUNNING_IN_CONTAINER=1

# API will run on port 8000 by default
EXPOSE 8000/tcp

# No healthcheck by default
HEALTHCHECK NONE

# But feel free to add arguments and options as needed when doing a docker run
ENTRYPOINT ["uv", "run", "--all-extras", "--no-dev", "starbridge"]
