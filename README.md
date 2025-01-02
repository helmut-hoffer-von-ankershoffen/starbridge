# [PRE-ALPHA] ⭐ starbridge MCP server for Claude Desktop

[![License](https://img.shields.io/github/license/helmut-hoffer-von-ankershoffen/starbridge?logo=opensourceinitiative&logoColor=3DA639&labelColor=414042&color=A41831)
](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/starbridge.svg?logo=python&color=204361&labelColor=1E2933)](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/blob/main/noxfile.py)
[![CI](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/actions/workflows/test-and-report.yml/badge.svg)](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/actions/workflows/test-and-report.yml)
[![Read the Docs](https://img.shields.io/readthedocs/starbridge)](https://starbridge.readthedocs.io/)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=helmut-hoffer-von-ankershoffen_starbridge&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=helmut-hoffer-von-ankershoffen_starbridge)
[![Security](https://sonarcloud.io/api/project_badges/measure?project=helmut-hoffer-von-ankershoffen_starbridge&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=helmut-hoffer-von-ankershoffen_starbridge)
[![Maintainability](https://sonarcloud.io/api/project_badges/measure?project=helmut-hoffer-von-ankershoffen_starbridge&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=helmut-hoffer-von-ankershoffen_starbridge)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=helmut-hoffer-von-ankershoffen_starbridge&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=helmut-hoffer-von-ankershoffen_starbridge)
[![Coverage](https://codecov.io/gh/helmut-hoffer-von-ankershoffen/starbridge/graph/badge.svg?token=SX34YRP30E)](https://codecov.io/gh/helmut-hoffer-von-ankershoffen/starbridge)
[![Ruff](https://img.shields.io/badge/style-Ruff-blue?color=D6FF65)](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/blob/main/noxfile.py)
[![GitHub - Version](https://img.shields.io/github/v/release/helmut-hoffer-von-ankershoffen/starbridge?label=GitHub&style=flat&labelColor=1C2C2E&color=blue&logo=GitHub&logoColor=white)](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/releases)
![GitHub - Commits](https://img.shields.io/github/commit-activity/m/helmut-hoffer-von-ankershoffen/starbridge/main?label=commits&style=flat&labelColor=1C2C2E&color=blue&logo=GitHub&logoColor=white)
[![PyPI - Version](https://img.shields.io/pypi/v/starbridge.svg?label=PyPI&logo=pypi&logoColor=%23FFD243&labelColor=%230073B7&color=FDFDFD)](https://pypi.python.org/pypi/starbridge)
[![PyPI - Status](https://img.shields.io/pypi/status/starbridge?logo=pypi&logoColor=%23FFD243&labelColor=%230073B7&color=FDFDFD)](https://pypi.python.org/pypi/starbridge)
[![Docker - Version](https://img.shields.io/docker/v/helmuthva/starbridge?sort=semver&label=Docker&logo=docker&logoColor=white&labelColor=1354D4&color=10151B)](https://hub.docker.com/r/helmuthva/starbridge/tags)
[![Docker - Size](https://img.shields.io/docker/image-size/helmuthva/starbridge?sort=semver&arch=arm64&label=image&logo=docker&logoColor=white&labelColor=1354D4&color=10151B)](https://hub.docker.com/r/helmuthva/starbridge/)
<!---
[![ghcr.io - Version](https://ghcr-badge.egpl.dev/helmut-hoffer-von-ankershoffen/starbridge/tags?color=%2344cc11&ignore=0.0%2C0%2Clatest&n=3&label=ghcr.io&trim=)](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/pkgs/container/starbridge)
[![ghcr.io - Sze](https://ghcr-badge.egpl.dev/helmut-hoffer-von-ankershoffen/starbridge/size?color=%2344cc11&tag=latest&label=size&trim=)](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/pkgs/container/starbridge)
-->
> ⚠️ **WARNING**: This project is currently in pre-alpha phase, i.e. partly functional. Feel free to already watch or star the repository to stay updated on its progress.

Integrates Claude Desktop with the web, Atlassian Confluence, and (later on) Google Workspace.

1. **Make Claude a team member**: Makes Claude an informed member of your organisation by accessing your organization's key knowledge resources.
2. **Integrate research and knowlege management**: Enables your teams to contribute, refine, and maintain your organisation's knowledge resources within Claude - seamlessly integrating research and sharing knowledge.
3. **Improve efficiency**: Automate repetitive workflows such as generating Confluence pages from Google Docs.

## Qualities

* [Complete reference documenation](https://starbridge.readthedocs.io/en/latest/reference_index.html) on Read the Docs
* [High test coverage](https://app.codecov.io/gh/helmut-hoffer-von-ankershoffen/starbridge) including unit and E2E tests (reported on Codecov)
* Matrix tested with [Python 3.11, 3.12 and 3.13](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/blob/main/noxfile.py) to ensure compatibility (powered by [Nox](https://nox.thea.codes/en/stable/))
* 100% compliant with modern linting and formatting standards (powered by [Ruff](https://github.com/astral-sh/ruff))
* 100% up-to-date dependencies (monitored by [Renovate](https://github.com/renovatebot/renovate))
* [A-grade code quality](https://sonarcloud.io/summary/new_code?id=helmut-hoffer-von-ankershoffen_starbridge) in security, maintainability, and reliability (verified by SonarQube)
* 1-liner for installation and execution of command line interface (CLI) via [uv(x)](https://github.com/astral-sh/uv) or [Docker](https://hub.docker.com/r/helmuthva/starbridge/tags)
* Setup for developing inside a [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers) included (supports VSCode and GitHub Codespaces)

## Example Prompts

* "Create a page about road cycling, focusing on Canyon bikes, in the personal confluence space of Helmut."

## Setup

```uvx starbridge install``` - that's all.

Prequisites:
- You are running Mac OS X
- You already have the uv package manager installed
- You already have Claude Desktop for Mac OS X installed
- You don't care for the imaging extra

If you (possibly) need to install homebrew, uv, and care for all extras:

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

Starbridge can be [run within Docker](https://starbridge.readthedocs.io/en/latest/docker.html).

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

Please read our [Contributing Guidelines](https://starbridge.readthedocs.io/en/latest/contributing.html) for how to setup for development, and before making a pull request.

## Resources

* [MCP Press release](https://www.anthropic.com/news/model-context-protocol)
* [MCP Specification and SDKs](https://github.com/modelcontextprotocol)
* [MCP Info to amend Claude's context](https://modelcontextprotocol.io/llms-full.txt)

## Star History

<a href="https://star-history.com/#helmut-hoffer-von-ankershoffen/starbridge&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=helmut-hoffer-von-ankershoffen/starbridge&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=helmut-hoffer-von-ankershoffen/starbridge&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=helmut-hoffer-von-ankershoffen/starbridge&type=Date" />
 </picture>
</a>
