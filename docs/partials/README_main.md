Integrates Claude Desktop with the web, Google and Atlassian workspaces.

1. **Make Claude a team member**: Makes Claude an informed member of your
   organisation by accessing your organization's key knowledge resources.
2. **Integrate research and knowlege management**: Enables your teams to
   contribute, refine, and maintain your organisation's knowledge resources
   within Claude - seamlessly integrating research and sharing knowledge.
3. **Improve efficiency**: Automate repetitive workflows such as generating
   Confluence pages from Google Docs.

## Operational Excellence

- [Complete reference documenation](https://starbridge.readthedocs.io/en/latest/reference.html)
  on Read the Docs
- [Transparent test coverage](https://app.codecov.io/gh/helmut-hoffer-von-ankershoffen/starbridge)
  including unit and E2E tests (reported on Codecov)
- Matrix tested with
  [multiple python versions](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/blob/main/noxfile.py)
  to ensure compatibility (powered by [Nox](https://nox.thea.codes/en/stable/))
- Compliant with modern linting and formatting standards (powered by
  [Ruff](https://github.com/astral-sh/ruff))
- Up-to-date dependencies (monitored by
  [Renovate](https://github.com/renovatebot/renovate) and
  [GitHub Dependabot](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/security/dependabot))
- [A-grade code quality](https://sonarcloud.io/summary/new_code?id=helmut-hoffer-von-ankershoffen_starbridge)
  in security, maintainability, and reliability with low technical debt and
  codesmell (verified by SonarQube)
- Additional code security checks using
  [GitHub CodeQL](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/security/code-scanning)
- [Security Policy](SECURITY.md)
- 1-liner for installation and execution of command line interface (CLI) via
  [uv(x)](https://github.com/astral-sh/uv) or
  [Docker](https://hub.docker.com/r/helmuthva/starbridge/tags)
- Setup for developing inside a
  [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers)
  included (supports VSCode and GitHub Codespaces)

## Example Prompts

- "Create a page about road cycling, focusing on Canyon bikes, in the personal
  confluence space of Helmut."

## Setup

`uvx starbridge install` - that's all.

Prequisites:

- You are running Mac OS X
- You already have the uv package manager installed
- You already have Claude Desktop for Mac OS X installed
- You don't care for the imaging extra

If you need to first install homebrew and uv - and care for all extras:

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
  source $HOME/.local/bin/env
fi
uvx --with "starbridge[imaging]" starbridge install # Install starbridge, including configuration and injection into Claude Desktop App
```

Starbridge can be
[run within Docker](https://starbridge.readthedocs.io/en/latest/docker.html).

## MCP Server

Starbridge implements the
[MCP Server](https://modelcontextprotocol.io/docs/concepts/architecture)
interface, with Claude acting as an MCP client.

### Resources

[TODO: Document resources exposed to Claude Desktop]

### Prompts

[TODO: Document prompts exposed to Claude Desktop]

### Tools

[TODO: Document tools exposed to Claude Desktop]

## CLI

[TODO: Document CLI commands]
