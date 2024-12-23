# [PRE-ALPHA] starbridge MCP server for Claude Desktop

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) 
[![CI](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/actions/workflows/test.yml/badge.svg)](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/actions/workflows/test.yml) 
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=helmut-hoffer-von-ankershoffen_starbridge&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=helmut-hoffer-von-ankershoffen_starbridge)
[![Security](https://sonarcloud.io/api/project_badges/measure?project=helmut-hoffer-von-ankershoffen_starbridge&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=helmut-hoffer-von-ankershoffen_starbridge)
[![Maintainability](https://sonarcloud.io/api/project_badges/measure?project=helmut-hoffer-von-ankershoffen_starbridge&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=helmut-hoffer-von-ankershoffen_starbridge)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=helmut-hoffer-von-ankershoffen_starbridge&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=helmut-hoffer-von-ankershoffen_starbridge)
[![Coverage](https://codecov.io/gh/helmut-hoffer-von-ankershoffen/starbridge/graph/badge.svg?token=SX34YRP30E)](https://codecov.io/gh/helmut-hoffer-von-ankershoffen/starbridge)
[![GitHub](https://img.shields.io/github/v/release/helmut-hoffer-von-ankershoffen/starbridge?style=flat&labelColor=1C2C2E&color=C96329&logo=GitHub&logoColor=white)](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/releases)
[![PyPI](https://img.shields.io/pypi/v/starbridge.svg?logo=pypi)](https://pypi.python.org/pypi/starbridge)
[![Docker](https://badgen.net/docker/size/helmuthva/starbridge?icon=docker&label=image%20size)](https://hub.docker.com/r/helmuthva/starbridge/)
![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/m/helmut-hoffer-von-ankershoffen/starbridge/main?logo=GitHub&logoColor=white)


> ⚠️ **WARNING**: This project is currently in pre-alpha phase, i.e. partly functional. Feel free to watch or star the repository to stay updated on its progress.

Integrates Claude Desktop with Google and Atlassian workspaces.

This integration serves two main purposes:
1. **Make Claude smarter**: Makes Claude an informed member of your organisation by accessing your organization's key knowledge resources.
2. **Integrate research and knowlege management**: Enables your teams to contribute, refine, and maintain your organisation's knowledge resources within Claude.
3. **Improve efficiency**: Automate workflows such as generating Confluence pages from Google Docs, or vice versa.

## Example Prompts

* "Create a page about road cycling, focusing on Canyon bikes, in the personal confluence space of Helmut."

## Setup

```shell
if [[ "$OSTYPE" == "darwin"* ]]; then # Install dependencies for macOS X
  if ! command -v brew &> /dev/null; then # Install Homebrew if not present
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  fi
  brew install cairo
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then # Install dependencies for Linux
  sudo apt-get update -y && sudo apt-get install curl libcairo2 -y
fi
if ! command -v uvx &> /dev/null; then # Install uv package manager if not present
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi
uvx starbridge install # Install starbridge, including configuration and injection into Claude Desktop App
```

See [here](DOCKER.md) for running Starbridge in a Docker container.

## MCP Server

Starbridge implements the [MCP Server](https://modelcontextprotocol.io/docs/concepts/architecture) interface, with Claude acting as an MCP client.

### Resources

[TODO: Document resources exposed to Claude Desktop]

### Prompts

[TODO: Document prompts exposed to Claude Desktop]

### Tools

[TODO: Document tools exposed to Claude Desktop]

## CLI

[TODO: Document CLI commands]

## Contributing

Please read our [Contributing Guidelines](CONTRIBUTING.md) for how to setup for development, and before making a pull request.

## Resources

* [MCP Press release](https://www.anthropic.com/news/model-context-protocol)
* [MCP Specification and SDKs](https://github.com/modelcontextprotocol)
* [MCP Info to amend Claude's context](https://modelcontextprotocol.io/llms-full.txt)
* [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)

## Star History

<a href="https://star-history.com/#helmut-hoffer-von-ankershoffen/starbridge&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=helmut-hoffer-von-ankershoffen/starbridge&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=helmut-hoffer-von-ankershoffen/starbridge&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=helmut-hoffer-von-ankershoffen/starbridge&type=Date" />
 </picture>
</a>
