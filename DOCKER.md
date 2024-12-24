# Starbridge within Docker

## Install for Claude

Executing the below will (1) pull the Starbridge Docker image from [Docker.io](https://hub.docker.com/repository/docker/helmuthva/starbridge), (2) prompt you for required configuration settings, and (3) update the configuration of the Claude Desktop application to connect with the Starbridge MCP server. 

```bash
case "$OSTYPE" in
  darwin*) SRC="$HOME/Library/Application Support/Claude" ;;
  linux*) SRC="$HOME/.config/Claude" ;;
  win32*|cygwin*|msys*) SRC="%APPDATA%/Claude" ;;
  *) echo "Unsupported OS"; exit 1 ;;
esac
docker run -it --pull always --mount type=bind,src="$SRC",dst="/Claude" helmuthva/starbridge install
```

Note:
* Restart the Claude Desktop application for the updated configuration to take effect.
* [helmuthva/hva](https://hub.docker.com/repository/docker/helmuthva/starbridge) is a multi-arch image, supporting both x86 and Arm64 chips.
* Not tested on Windows


## Running standalone

Show commands and their help

```bash
docker run helmuthva/starbridge --help
```

Determine health 

```bash
docker run helmuthva/starbridge health
```

This will indicate which environment variables to set.

```bash
docker run \
  -e STARBRIDGE_ATLASSIAN_URL=https://your-domain.atlassian.net \
  -e STARBRIDGE_ATLASSIAN_EMAIL_ADDRESS=your-email@domain.com \
  -e STARBRIDGE_ATLASSIAN_API_TOKEN=your-api-token \
  helmuthva/starbridge health
```

Alternatively manage the settings via an .env file on the host

```bash
# cp .env.example .env && nano .env
docker run --env-file=.env helmuthva/starbridge health
```

Run inspector to interact with the server via the MCP protocol - point your browser to https://127.0.0.1:5173.
```bash
docker run --env-file=.env -it  -p 127.0.0.1:5173:5173 -p 127.0.0.1:3000:3000 helmuthva/starbridge mcp inspect
```

List Confluence spaces:

```bash
docker run --env-file=.env helmuthva/starbridge confluence space list
```

Start the MCP Server on given host and port

```bash
docker run --env-file=.env helmuthva/starbridge mcp serve --host=localhost --port=8080
```

## Build and install Docker image from source

Build the Docker image:
```bash
docker build -t starbridge .
```

Install the locally built Docker image
```bash
case "$OSTYPE" in
  darwin*) SRC="$HOME/Library/Application Support/Claude" ;;
  linux*) SRC="$HOME/.config/Claude" ;;
  win32*|cygwin*|msys*) SRC="%APPDATA%/Claude" ;;
  *) echo "Unsupported OS"; exit 1 ;;
esac
docker run -it --mount type=bind,src="$SRC",dst="/Claude" starbridge install --image starbridge
```

Enter starbridge container via bash for inspection:
```bash
docker run --env-file=.env -it --entrypoint bash starbridge
```

Enter running starbridge container:

```bash
docker exec -it $(docker ps | awk '$2 ~ /starbridge/ {print $1}') bash
```

Check logs:
```bash
docker logs -f $(docker ps | awk '$2 ~ /starbridge/ {print $1}')
```

Run MCP Inspector connected to Starbridge MCP Server
```bash
docker run --env-file=.env -it  -p 127.0.0.1:5173:5173 -p 127.0.0.1:3000:3000 starbridge mcp inspect
```

Or use docker compose

File .env is passed through

```bash
docker compose up # starts inspector
docker compose run starbridge --help
docker compose run starbridge health
docker compose run starbridge info
docker compose run starbridge mcp tools
```
