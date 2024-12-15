import importlib.metadata
import os
import pathlib
import sys
from typing import Annotated, Any

import typer
from dotenv import dotenv_values, load_dotenv
from rich.prompt import Prompt

import starbridge.claude
import starbridge.confluence
import starbridge.mcp
from starbridge.utils.console import console

load_dotenv()

__version__ = importlib.metadata.version("starbridge")

cli = typer.Typer(
    name="Starbridge CLI",
    help=f"Starbride (Version: {__version__})",
    epilog="Built with love in Berlin by Helmut Hoffer von Ankershoffen",
)


@cli.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Run MCP Server - alias for 'mcp serve'"""
    if ctx.invoked_subcommand is None:
        starbridge.mcp.serve()


@cli.command()
def health():
    """Health of starbridge and dependencie"""
    dependencies = {
        "confluence": starbridge.confluence.Service().health(),
        "claude": starbridge.claude.Application.health(),
    }
    healthy = all(status == "UP" for status in dependencies.values())
    console.print({"healthy": healthy, "dependencies": dependencies})


@cli.command()
def info():
    """Info about Starbridge"""
    data: dict[str, Any] = {
        "version": __version__,
        "path": _get_starbridge_path(),
        "development_mode": _is_development_mode(),
    }
    data["confluence"] = starbridge.confluence.Service().info()
    data["claude"] = starbridge.claude.Application().info()
    data["env"] = _get_starbridge_env()
    console.print(data)


@cli.command()
def configure():
    """Generate .env file for Starbridge"""
    if not _is_development_mode():
        raise Exception("This command is only available in development mode")

    starbridge_path = pathlib.Path(_get_starbridge_path())
    env_example_path = starbridge_path / ".env.example"
    env_path = starbridge_path / ".env"

    if not env_example_path.exists():
        raise Exception(".env.example file not found")

    example_values = dotenv_values(env_example_path)
    current_values = dotenv_values(env_path) if env_path.exists() else {}

    new_values = {}
    for key in example_values:
        default_value = current_values.get(key, example_values[key])
        value = Prompt.ask(
            f"Enter value for {key}",
            default=default_value if default_value else None,
            password="TOKEN" in key or "SECRET" in key,
        )
        new_values[key] = value

    with open(env_path, "w") as f:
        for key, value in new_values.items():
            # Try to convert to number, if it fails, it's not a number
            try:
                float(value)
                f.write(f"{key}={value}\n")
            except ValueError:
                f.write(f'{key}="{value}"\n')


@cli.command()
def install(
    atlassian_url: Annotated[
        str,
        typer.Option(
            prompt="Base url of your Confluence and Jira installation",
            help="Base url of your Confluence and Jira installation, e.g. https://your-domain.atlassian.net",
        ),
    ] = os.environ.get("STARBRIDGE_ATLASSIAN_URL", "https://your-domain.atlassian.net"),
    atlassian_email_address: Annotated[
        str,
        typer.Option(
            prompt="Email address of your Atlassian account",
            help="Email address of your Atlassian account, e.g. you@your-domain.com",
        ),
    ] = os.environ.get("STARBRIDGE_ATLASSIAN_EMAIL_ADDRESS", "you@your-domain.com"),
    atlassian_api_token: Annotated[
        str,
        typer.Option(
            prompt="Go to https://id.atlassian.com/manage-profile/security/api-tokens to create an API token for starbridge",
            help="API token of your Atlassian account, go to https://id.atlassian.com/manage-profile/security/api-tokens to create one",
        ),
    ] = os.environ.get("STARBRIDGE_ATLASSIAN_API_TOKEN", "YOUR_TOKEN"),
    restart_claude: bool = True,
):
    """Install starbridge within Claude Desktop application by adding to configuration and restarting Claude Desktop app"""
    if starbridge.claude.Application.install_mcp_server(
        _generate_mcp_server_config(
            atlassian_url, atlassian_email_address, atlassian_api_token
        ),
        restart=restart_claude,
    ):
        console.print("Starbridge insalled with Claude Desktop application.")
    else:
        console.print("Starbridge was already installed", style="warning")


@cli.command()
def uninstall():
    """Install starbridge from Claude Desktop application by removing from configuration and restarting Claude Desktop app"""
    if starbridge.claude.Application.uninstall_mcp_server():
        console.print("Starbridge uninstalled from Claude Destkop application.")
    else:
        console.print("Starbridge was no installed", style="warning")


def _is_development_mode():
    return "uvx" not in sys.argv[0].lower()


def _get_starbridge_path() -> str:
    return str(pathlib.Path(__file__).parent.parent.parent)


def _get_starbridge_env():
    """Get environment variables starting with STARBRIDGE_"""
    return {k: v for k, v in os.environ.items() if k.startswith("STARBRIDGE_")}


def _generate_mcp_server_config(
    atlassian_url: str,
    atlassian_email_address: str,
    atlassian_api_token: str,
) -> dict:
    """Generate configuration file for Starbridge"""
    env = {
        "STARBRIDGE_ATLASSIAN_URL": atlassian_url,
        "STARBRIDGE_ATLASSIAN_EMAIL_ADDRESS": atlassian_email_address,
        "STARBRIDGE_ATLASSIAN_API_TOKEN": atlassian_api_token,
    }
    if _is_development_mode():
        return {
            "command": "uv",
            "args": [
                "--directory",
                _get_starbridge_path(),
                "run",
                "starbridge",
            ],
            "env": env,
        }
    return {
        "command": "uvx",
        "args": [
            "starbridge",
        ],
        "env": env,
    }


cli.add_typer(
    starbridge.mcp.cli,
    name="mcp",
    help="MCP operations",
)
cli.add_typer(
    starbridge.confluence.cli, name="confluence", help="Confluence operations"
)
cli.add_typer(starbridge.claude.cli, name="claude", help="Claude operations")

if __name__ == "__main__":
    cli()
