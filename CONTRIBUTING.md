# Contributing

Thank you for considering contributing to Starbridge!

## Setup

Install or update tools required for development:

```shell
# Install Homebrew, uv package manager, copier and further dev tools
curl -LsSf https://raw.githubusercontent.com/helmut-hoffer-von-ankershoffen/oe-python-template/HEAD/install.sh | sh
```

[Create a fork](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/fork)
and clone your fork using `git clone URL_OF_YOUR_CLONE`. Then change into the
directory of your local Starbridge repository with `cd starbridge`.

If you are one of the committers of
https://github.com/helmut-hoffer-von-ankershoffen/starbridge you can directly
clone via
`git clone git@github.com:helmut-hoffer-von-ankershoffen/starbridge.git` and
`cd starbridge`.

## Configuration

You can use the following helper command to create the .env file. This will
prompt you for the required configuration values.

```bash
uv run starbridge configure # creates .env file
```

You can validate starbridge is working correctly by checking the health endpoint

```bash
uv run starbridge health # shows healtiness of starbridge including dependencies
```

To see all commands starvridge offers you can call `uv run starbridge --help`

## Debugging

Inspect starbridge using the MCP inspector

```bash
uv run starbridge mcp inspect
```

Upon launching, the Inspector will display a URL that you can access in your
browser to begin debugging. Environment values are loaded from the `.env` file
generated in the previous step

## Installing the development version of starbridge with Claude Desktop application

You can use the following helper command to install the development version of
starbridge with Claude Desktop application. This will amend the configuration
file of Claude Desktop to reference your local repository, and restart Claude
Desktop.

```bash
uv run starbridge install
```

## Code and configuration changes

For the Claude Desktop app to pick up code changes to starbridge restart the
Claude Desktop application with `uv run starbridge claude restart`.

If you added additional configuration keys in .env.template, run
`uv run starbridge configure` again, to update the .env file. After that run
`uv run starbridge install` to install the updated configuration with the Claude
Desktop application.

To show the configuration of starbridge within Claude, you can use
`uv run starbridge claude config`.

## Directory Layout

```
├── Makefile               # Central entrypoint for build, test, release and deploy
├── noxfile.py             # Noxfile for running tests in multiple python environments and other tasks
├── .pre-commit-config.yaml # Definition of hooks run on commits
├── .github/               # GitHub specific files
│   ├── workflows/         # GitHub Actions workflows
│   ├── prompts/           # Custom prompots for GitHub Copilot
│   └── copilot-instructions.md # Insructions for GitHub Copilot
├── .vscode/               # Recommended VSCode settings and extensions
├── .env                   # Environment variables, on .gitignore
├── .env.example           # Example environment variables
src/starbridge/            # Source code
tests/                   # Unit and E2E tests
docs/                    # Documentation
├── partials/*.md        # Partials to compile README.md,  _main partial included in HTML and PDF documentation
├── ../README.md         # Compiled README.md shown on GitHub
├── source/*.rst         # reStructuredText files used to generate HTML and PDF documentation
├── ../*.md              # Markdown files shown on GitHub and imported by .rst files
├── source/conf.py       # Sphinx configuration used to generate HTML and PDF documentation
├── build/html/*         # Generated HTML documentation as multiple pages
├── build/singlehtml/index.html # HTML documentation as a single page
└── build/latex/starbridge.pdf # PDF manual - generate with make docs pdf
reports/                 # Compliance reports for auditing
├── junit.xml            # Report of executions
├── mypy_junit.xml       # Report of executions
├── coverage.xml         # Test coverage in XML format
├── coverage_html        # Report of test coverage in HTML format
├── licenses.csv         # List of dependencies and their license types
├── licenses.json        # .json file with dependencies their license types
└── licenses_grouped.json  # .json file with dependencies grouped by license type
```

## Build, Run and Release

### Setup project specific development environment

```shell
make setup
```

Don't forget to configure your `.env` file with the required environment
variables.

Notes:

1. .env.example is provided as a template, use `cp .env.example .env` and edit
   `.env` to create your environment.
2. .env is excluded from version control, so feel free to add secret values.

### Build

```shell
make        # Runs primary build steps, i.e. formatting, linting, testing, building HTML docs and distribution, auditing
make help   # Shows help with additional build targets, e.g. to build PDF documentation, bump the version to release etc.
```

Notes:

1. Primary build steps defined in `noxfile.py`.
2. Distribution dumped into `dist/`
3. Documentation dumped into `docs/build/html/` and `docs/build/latex/`
4. Audit reports dumped into `reports/`

### Run the CLI

```shell
uv run starbridge # shows help
```

### Commit and Push your changes

```shell
git add .
git commit -m "feat(user): added new api endpoint to offboard user"
git push
```

Notes:

1. [pre-commit hooks](https://pre-commit.com/) will run automatically on commit
   to ensure code quality.
2. We use the conventional commits format - see the
   [code style guide](CODE_STYLE.md) for the mandatory commit message format.

### Publish Release

```shell
make bump   # Patch release
make minor  # Patch release
make major  # Patch release
make x.y.z  # Targeted release
```

Notes:

1. Changelog generated automatically
2. Publishes to PyPi, Docker Registries, Read The Docs, Streamlit and Auditing
   services

## Advanced usage

### Running GitHub CI Workflow locally

```shell
make act
```

Notes:

1. Workflow defined in `.github/workflows/*.yml`
2. test-and-report.yml calls all build steps defined in noxfile.py

### Pinning GitHub Actions

```shell
pinact run  # See https://dev.to/suzukishunsuke/pin-github-actions-to-a-full-length-commit-sha-for-security-2n7p
```

## Update from Template

Update project to latest version of
[oe-python-template](https://github.com/helmut-hoffer-von-ankershoffen/oe-python-template)
template.

```shell
make update_from_template
```

## Pull Request Guidelines

1. Before starting to write code read the [code style](CODE_STYLE.md) document
   for mandatory coding style requirements.
2. **Pre-Commit Hooks:** We use pre-commit hooks to ensure code quality. Please
   install the pre-commit hooks by running `uv run pre-commit install`. This
   ensure all tests, linting etc. pass locally before you can commit.
3. **Squash Commits:** Before submitting a pull request, please squash your
   commits into a single commit.
4. **Signed Commits:** Use
   [signed commits](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits).
5. **Branch Naming:** Use descriptive branch names like `feature/your-feature`
   or `fix/issue-number`.
6. **Testing:** Ensure new features have appropriate test coverage.
7. **Documentation:** Update documentation to reflect any changes or new
   features.
