# Contributing to starbridge

Thank you for considering contributing to starbridge!

## Setup

Clone this repository: ```git clone git@github.com:helmut-hoffer-von-ankershoffen/starbridge.git````

Install the dependencies:

### macOS

```shell
brew install jq xmllint act           # tooling
uv run pre-commit install             # see https://pre-commit.com/
```

### Linux

Notes:

- Not yet validated
- .github/workflows/ci.yml might provide further information

```shell
sudo sudo apt install -y curl jq xsltproc   # tooling
curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash # act
uv run pre-commit install                   # see https://pre-commit.com/
```

## Claude Desktop

Step 1: Open configuration file of Claude Desktop:
- MacOS: `code ~/Library/Application\ Support/Claude/claude_desktop_config.json`
- Windows: `code %APPDATA%/Claude/claude_desktop_config.json`

Step 2: Add/replace the starbridge configuration to reference your local repository. Replace `{{DIRECTORY_OF_YOUR_LOCAL_REPOSITORY}}` with the path to your local repository.

<details>
  <summary>Development/Unpublished Servers Configuration</summary>
  ```
  "mcpServers": {
    "starbridge": {
      "command": "uv",
      "args": [
        "--directory",
        "{{DIRECTORY_OF_YOUR_LOCAL_REPOSITORY}}",
        "run",
        "starbridge",
        "serve"
      ]
    }
  }
  ```
</details>

## Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).


You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory {{DIRECTORY_OF_YOUR_LOCAL_REPOSITORY}} run starbridge serve
```

Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.

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
