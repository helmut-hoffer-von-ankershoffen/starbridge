Integrates Claude Desktop with the web, Google and Atlassian workspaces.

Use Cases:
1) Fast and easy to use project setup
2) Consistent update of already scaffolded projects to benefit from new and improved features.
3) Dummy CLI application and service demonstrating example usage of the generated directory structure and build pipeline

## Scaffolding

**Step 1**: Install uv package manager and copier
```shell
if [[ "$OSTYPE" == "darwin"* ]]; then                 # Install dependencies for macOS X
  if ! command -v brew &> /dev/null; then             ## Install Homebrew if not present
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then            # Install dependencies for Linux
  sudo apt-get update -y && sudo apt-get install curl -y # Install curl
fi
if ! command -v uvx &> /dev/null; then                # Install uv package manager if not present
  curl -LsSf https://astral.sh/uv/install.sh | sh
  source $HOME/.local/bin/env
fi
uv tool install copier                                # Install copier as global tool
```

**Step 2**: Now create an empty repository on GitHubm, clone to your local machine, and change into it's directory.

**Step 3**: Scaffold the project
```shell
copier copy gh:helmut-hoffer-von-ankershoffen/oe-python-template .
```
**Step 4**: Setup the local environment

```shell
uv run nox -s setup_dev
```

**Step 5**: Perform initial commit and push
```shell
git add .
git commit -m "feat: Initial commit"
git push
```

Visit your GitHub repository and check the Actions tab. The CI workflow should fail at the SonarQube step,
as this external service is not yet configured for our new repository.

**Step 6**: Follow the [instructions](SERVICE_CONNECTIONS.md) to wire up
external services such as Cloudcov, SonarQube Cloud, Read The Docs, Docker.io, GHCR.io and Streamlit Community Cloud.

**Step 7**: Release the first versions
```shell
./bump
```
Notes:
* You can remove this section post having successfully scafolded your project.
* The following sections refer to the dummy application and service provided by this template.
  Use them as inspiration and adapt them to your own project.

## Overview

Adding Starbridge to your project as a dependency is easy.

```shell
uv add starbridge             # add dependency to your project
```

If you don't have uv installed follow [these instructions](https://docs.astral.sh/uv/getting-started/installation/). If you still prefer pip over the modern and fast package manager [uv](https://github.com/astral-sh/uv), you can install the library like this:

```shell
pip install starbridge        # add dependency to your project
```

Executing the command line interface (CLI) in an isolated Python environment is just as easy:

```shell
uvx starbridge hello-world     # prints "Hello, world! [..]"
uvx starbridge serve           # serves webservice API
uvx starbridge serve --port=4711 # serves webservice API on port 4711
```

Notes:
* The API is versioned, mounted at ```/api/v1``` resp. ```/api/v2```
* While serving the webservice API go to [http://127.0.0.1:8000/api/v1/hello-world](http://127.0.0.1:8000/api/v1/hello-world) to see the respons of the ```hello-world``` operation.
* Interactive documentation is provided at [http://127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs)


The CLI provides extensive help:

```shell
uvx starbridge --help                # all CLI commands
uvx starbridge hello-world --help    # help for specific command
uvx starbridge echo --help
uvx starbridge openapi --help
uvx starbridge serve --help
```


## Operational Excellence

This project is designed with operational excellence in mind, using modern Python tooling and practices. It includes:

* Various examples demonstrating usage:
  - [Simple Python script](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/blob/main/examples/script.py)
  - [Streamlit web application](https://starbridge.streamlit.app/) deployed on [Streamlit Community Cloud](https://streamlit.io/cloud)
  - [Jupyter](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/blob/main/examples/notebook.ipynb) and [Marimo](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/blob/main/examples/notebook.py) notebook
* [Complete reference documentation](https://starbridge.readthedocs.io/en/latest/reference.html) on Read the Docs
* [Transparent test coverage](https://app.codecov.io/gh/helmut-hoffer-von-ankershoffen/starbridge) including unit and E2E tests (reported on Codecov)
* Matrix tested with [multiple python versions](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/blob/main/noxfile.py) to ensure compatibility (powered by [Nox](https://nox.thea.codes/en/stable/))
* Compliant with modern linting and formatting standards (powered by [Ruff](https://github.com/astral-sh/ruff))
* Up-to-date dependencies (monitored by [Renovate](https://github.com/renovatebot/renovate) and [GitHub Dependabot](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/security/dependabot))
* [A-grade code quality](https://sonarcloud.io/summary/new_code?id=helmut-hoffer-von-ankershoffen_starbridge) in security, maintainability, and reliability with low technical debt and codesmell (verified by SonarQube)
* Additional code security checks using [GitHub CodeQL](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/security/code-scanning)
* [Security Policy](SECURITY.md)
* [License](LICENSE) compliant with the Open Source Initiative (OSI)
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
