# Contributing to starbridge

Thank you for considering contributing to starbridge!

## Development Environment Setup

Clone this GitHub repository via ```git clone git@github.com:helmut-hoffer-von-ankershoffen/starbridge.git``` and change into the directory of your local starbridge repository: ```cd starbridge```

Install the dependencies:

### macOS

```shell
if ! command -v brew &> /dev/null; then # if Homebrew package manager not present ...
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" # ... install it
else
  which brew # ... otherwise inform where brew command was found
fi
# Install required tools if not present
which jq &> /dev/null || brew install jq
which xmllint &> /dev/null || brew install xmllint
which act &> /dev/null || brew install act
uv run pre-commit install             # install pre-commit hooks, see https://pre-commit.com/
```

### Linux

Notes:

- Not yet validated
- .github/workflows/test.yml might provide further information

```shell
sudo sudo apt install -y curl jq libxml2-utils libcairo2 gnupg2 npm  # tooling
curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash # act
uv run pre-commit install                   # see https://pre-commit.com/
```

## Configuration

You can use the following helper command to create the .env file. This will prompt you for the required configuration values.

```bash
uv run starbridge configure # creates .env file
```

You can validate starbridge is working correctly by checking the health endpoint

```bash
uv run starbridge health # shows healtiness of starbridge including dependencies
```

To see all commands starvridge offers you can call ```uv run starbridge --help```

## Debugging

Inspect starbridge using the MCP inspector

```bash
uv run starbridge mcp inspect
```

Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging. Environment values are loaded from the ```.env``` file generated in the previous step

## Installing the development version of starbridge with Claude Desktop application

You can use the following helper command to install the development version of starbridge with Claude Desktop application. This will amend the configuration file of Claude Desktop to reference your local repository, and restart Claude Desktop.

```bash
uv run starbridge install
```

## Code and configuration changes

For the Claude Desktop app to pick up code changes to starbridge restart the Claude Desktop application with ```uv run starbridge claude restart```.

If you added additional configuration keys in .env.template, run ```uv run starbridge configure``` again, to update the .env file. After that run ```uv run starbridge install``` to install the updated configuration with the Claude Desktop application.

To show the configuration of starbridge within Claude, you can use ```uv run starbridge claude config```.

## Running all build steps

All build steps are defined in `noxfile.py`.

```shell
uv run nox
```

You can run individual build steps - called sessions in nox as follows:

```shell
uv run nox -s test      # run tests
uv run nox -s lint      # run formatting and linting
uv run nox -s audit     # run security and license audit, inc. sbom generation
```

## Running GitHub CI workflow locally

Notes:

- Workflow defined in .github/workflows/ci.yml
- Calls all build steps defined in noxfile.py

```shell
./github-action-run.sh
```

## Pull Request Guidelines

- **Pre-Commit Hooks:** We use pre-commit hooks to ensure code quality. Please install the pre-commit hooks by running `uv run pre-commit install`. This ensure all tests, linting etc. pass locally before you can commit.
- **Squash Commits:** Before submitting a pull request, please squash your commits into a single commit.
- **Branch Naming:** Use descriptive branch names like `feature/your-feature` or `fix/issue-number`.
- **Testing:** Ensure new features have appropriate test coverage.
- **Documentation:** Update documentation to reflect any changes or new features.
