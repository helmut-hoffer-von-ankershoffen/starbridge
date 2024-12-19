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
docker run -it --mount type=bind,src="$SRC",dst="/Claude" helmuthva/starbridge install
```

Note:
* Restart the Claude Desktop application for the updated configuration to take effect.
* [helmuthva/hva](https://hub.docker.com/repository/docker/helmuthva/starbridge) is a multi-arch image, supporting both x86 and Arm64 chips.
* Not tested on Windows


## Running standalone

Show commands and their help

```bash
docker run \
  -e STARBRIDGE_ATLASSIAN_URL=https://your-domain.atlassian.net \
  -e STARBRIDGE_ATLASSIAN_EMAIL_ADDRESS=your-email@domain.com \
  -e STARBRIDGE_ATLASSIAN_API_TOKEN=your-api-token \
  helmuthva/starbridge --help
```

List Confluence spaces:

```bash
docker run \
  -e STARBRIDGE_ATLASSIAN_URL=https://your-domain.atlassian.net \
  -e STARBRIDGE_ATLASSIAN_EMAIL_ADDRESS=your-email@domain.com \
  -e STARBRIDGE_ATLASSIAN_API_TOKEN=your-api-token \
  helmuthva/starbridge confluence space list
```

Start the MCP Server on given host and port

```bash
docker run \
  -e STARBRIDGE_ATLASSIAN_URL=https://your-domain.atlassian.net \
  -e STARBRIDGE_ATLASSIAN_EMAIL_ADDRESS=your-email@domain.com \
  -e STARBRIDGE_ATLASSIAN_API_TOKEN=your-api-token \
  helmuthva/starbridge mcp serve --host=localhost --port=8080
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
docker run -it --entrypoint bash starbridge
```

Enter running starbridge container:

```bash
docker exec -it $(docker ps | grep starbridge | awk '{print $1}') bash
```

Check logs:
```bash
docker logs -f $(docker ps | grep starbridge | awk '{print $1}')
```
