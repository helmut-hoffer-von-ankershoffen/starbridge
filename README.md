# [PRE-ALPHA] starbridge MCP server for Claude Desktop

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) 
[![Test](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/actions/workflows/test.yml/badge.svg)](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/actions/workflows/test.yml) 
[![codecov](https://codecov.io/gh/helmut-hoffer-von-ankershoffen/starbridge/graph/badge.svg?token=SX34YRP30E)](https://codecov.io/gh/helmut-hoffer-von-ankershoffen/starbridge)

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
  brew install curl cairo
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then # ... resp. Linux
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
# [MCP Info to amend Claude's context](https://modelcontextprotocol.io/llms-full.txt)
* [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)

## Star History

<a href="https://star-history.com/#helmut-hoffer-von-ankershoffen/starbridge&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=helmut-hoffer-von-ankershoffen/starbridge&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=helmut-hoffer-von-ankershoffen/starbridge&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=helmut-hoffer-von-ankershoffen/starbridge&type=Date" />
 </picture>
</a>