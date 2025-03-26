Integrates Claude Desktop with the web, Google and Atlassian workspaces.

1. **Make Claude a team member**: Makes Claude an informed member of your
   organisation by accessing your organization's key knowledge resources.
2. **Integrate research and knowlege management**: Enables your teams to
   contribute, refine, and maintain your organisation's knowledge resources
   within Claude - seamlessly integrating research and sharing knowledge.
3. **Improve efficiency**: Automate repetitive workflows such as generating
   Confluence pages from Google Docs.

## Example Prompts

- "Create a page about road cycling, focusing on Canyon bikes, in the personal
  confluence space of Helmut."

## Setup

If you already have [uv](https://astral.sh/uv) package manager and
[Claude Desktop](https://claude.ai/download) installed on your Mac:

```shell
# Installs starbridge in an isolated Python environment
# Auto-injects configuration into Claude Desktop
uvx starbridge install
```

If you first need to install uv:

```shell
if ! command -v brew &> /dev/null; then # Install Homebrew
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
brew install uv # Install uv via Homebrew
uvx starbridge install # Install starbridge via uv
```

If you want to install starbridge with the imaging extra

```shell
uvx --with "starbridge[imaging]" starbridge install
```

You can as well
[run Starbridge with Docker](https://starbridge.readthedocs.io/en/latest/docker.html).

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

## Operational Excellence

This project is designed with operational excellence in mind, using modern
Python tooling and practices. It includes:

1. [Complete reference documentation](https://starbridge.readthedocs.io/en/latest/reference.html)
   on Read the Docs
2. [Transparent test coverage](https://app.codecov.io/gh/helmut-hoffer-von-ankershoffen/starbridge)
   including unit and E2E tests (reported on Codecov)
3. Matrix tested with
   [multiple python versions](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/blob/main/noxfile.py)
   to ensure compatibility (powered by [Nox](https://nox.thea.codes/en/stable/))
4. Compliant with modern linting and formatting standards (powered by
   [Ruff](https://github.com/astral-sh/ruff))
5. Up-to-date dependencies (monitored by
   [Renovate](https://github.com/renovatebot/renovate) and
   [Dependabot](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/security/dependabot))
6. [A-grade code quality](https://sonarcloud.io/summary/new_code?id=helmut-hoffer-von-ankershoffen_starbridge)
   in security, maintainability, and reliability with low technical debt and
   codesmell (verified by SonarQube)
7. Additional code security checks using
   [CodeQL](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/security/code-scanning)
8. [Security Policy](SECURITY.md)
9. [License](LICENSE) compliant with the Open Source Initiative (OSI)
10. 1-liner for installation and execution of command line interface (CLI) via
    [uv(x)](https://github.com/astral-sh/uv) or
    [Docker](https://hub.docker.com/r/helmuthva/starbridge/tags)
11. Setup for developing inside a
    [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers)
    included (supports VSCode and GitHub Codespaces)
