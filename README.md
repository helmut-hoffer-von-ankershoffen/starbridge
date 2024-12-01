# [PLANNING] starbridge MCP server for Claude Desktop

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE.md)

> ⚠️ **WARNING**: This project is currently in early planning phase and not yet functional. Feel free to watch or star the repository to stay updated on its progress.


Integrates Cl aude Desktop with Google workspace and Atlassian workspaces.

This integration serves two main purposes:
1. **Make Claude smarter**: Makes Claude an informed member of your organisation by accessing your organization's key knowledge resources.
2. **Integrate research and knowlege management**: Enables your teams to contribute, refine, and maintain your organisation's knowledge resources within Claude.
3. **Improve efficiency**: Automate workflows such as generating Confluence pages from Google Docs, or vice versa.

## Examples

[TODO: A few examples of how to use the integration]

## Setup

Step 1: Open configuration of Claude Desktop:
- macOS: `code ~/Library/Application\ Support/Claude/claude_desktop_config.json`
- Windows: `code %APPDATA%/Claude/claude_desktop_config.json`

Step 2: Add the following configuration.

```json
"mcpServers": {
  "starbridge": {
    "command": "uvx",
    "args": [
      "starbridge",
      "serve"
    ]
  }
}
```

Notes:
1. Assumes you have Visual Studio Code installed and the `code` command is available.
2. In case you already have a section ```mcpServers```, just add the ```starbridge``` entry.

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

## References

[Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)