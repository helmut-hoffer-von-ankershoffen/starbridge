# Starbridge within Docker

## Install for Claude from image on docker.io

```... starbridge install``` will (1) interactively ask for required configuration settings, and (2) update Claude's configuration accordingly to start the Starbridge MCP Server. 

```bash
if [[ "$OSTYPE" == "darwin"* ]]; then # Install with host being macOS X
  docker run -it \
    --mount type=bind,src="$HOME/Library/Application Support/Claude",dst="/Claude" \
    helmuthva/starbridge install
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then # .. resp. Linux
  docker run -it \
    --mount type=bind,src="$HOME/.config/Claude",dst="/Claude" \
    helmuthva/starbridge install
elif [[ "$OSTYPE" == "windows"* ]]; then # resp. Windows
  docker run -it \
    --mount type=bind,src="%APPDATA%/Claude",dst="/Claude" \
    helmuthva/starbridge install
fi
```

Note:
(1) As Starbridge within Docker does is isolated from the Claude application process running on the host, you must manually restart the Claude Desktop application post installation for the updated configuration to take effect.
(2) Not tested on Windows

## Locally build Docker image from source

Build the Docker image:
```bash
docker build -t starbridge .
```

... with latest changes:
```bash
docker build --no-cache -t starbridge .
```

## Install for Claude from locally built container image

```... starbridge install``` will (1) interactively ask for required configuration settings, and (2) update Claude's configuration accordingly to start the Starbridge MCP Server. 

```bash
if [[ "$OSTYPE" == "darwin"* ]]; then # Install with host being macOS X
  docker run -it \
    --mount type=bind,src="$HOME/Library/Application Support/Claude",dst="/Claude" \
    starbridge install --image starbridge
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then # .. resp. Linux
  docker run -it \
    --mount type=bind,src="$HOME/.config/Claude",dst="/Claude" \
    starbridge install --image starbridge
elif [[ "$OSTYPE" == "windows"* ]]; then # resp. Windows
  docker run -it \
    --mount type=bind,src="%APPDATA%/Claude",dst="/Claude" \
    starbridge install --image starbridge
fi
```

Note:
(1) As Starbridge within Docker does is isolated from the Claude application process running on the host, you must manually restart the Claude Desktop application post installation for the updated configuration to take effect.
(2) Not tested on Windows

## Running manually

Start the MCP Server

```bash
docker run \
  -e STARBRIDGE_ATLASSIAN_URL=https://your-domain.atlassian.net \
  -e STARBRIDGE_ATLASSIAN_EMAIL_ADDRESS=your-email@domain.com \
  -e STARBRIDGE_ATLASSIAN_API_TOKEN=your-api-token \
  starbridge
```

Get help:

```bash
docker run \
  -e STARBRIDGE_ATLASSIAN_URL=https://your-domain.atlassian.net \
  -e STARBRIDGE_ATLASSIAN_EMAIL_ADDRESS=your-email@domain.com \
  -e STARBRIDGE_ATLASSIAN_API_TOKEN=your-api-token \
  starbridge --help
```

Run some command:

```bash
docker run \
  -e STARBRIDGE_ATLASSIAN_URL=https://your-domain.atlassian.net \
  -e STARBRIDGE_ATLASSIAN_EMAIL_ADDRESS=your-email@domain.com \
  -e STARBRIDGE_ATLASSIAN_API_TOKEN=your-api-token \
  starbridge confluence space list
```

## Accessing the Container Shell

Enter starbridge container via bash for inspection:
```bash
docker run -it --entrypoint bash starbridge
```

Enter running starbridge container:

```bash
docker exec -it $(docker ps | grep starbridge | awk '{print $1}') bash
```

## Development Tips

Check logs:
```bash
docker logs -f $(docker ps | grep starbridge | awk '{print $1}')
```
