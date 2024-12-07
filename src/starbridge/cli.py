import importlib.metadata
import os
import pathlib
import sys
from typing import Any

import typer
from dotenv import dotenv_values, load_dotenv
from rich.prompt import Prompt

import starbridge.claude
import starbridge.confluence
import starbridge.mcp

from .utils.console import console

load_dotenv()

__version__ = importlib.metadata.version("starbridge")

cli = typer.Typer(
    name="Starbridge CLI",
    help=f"Starbride (Version: {__version__})",
    epilog="Built with love in Berlin by Helmut Hoffer von Ankershoffen",
)


@cli.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Run MCP Server"""
    if ctx.invoked_subcommand is None:
        starbridge.mcp.serve()


def _is_development_mode():
    return "uvx" not in sys.argv[0].lower()


def _get_starbridge_path() -> str:
    return str(pathlib.Path(__file__).parent.parent.parent)


def _get_environment():
    """Get environment variables starting with STARBRIDGE_"""
    return {k: v for k, v in os.environ.items() if k.startswith("STARBRIDGE_")}


@cli.command()
def info():
    """Info about Starbridge Environment"""
    data: dict[str, Any] = {
        "version": __version__,
        "path": _get_starbridge_path(),
        "development_mode": _is_development_mode(),
    }
    data["confluence"] = starbridge.confluence.Service().info()
    data["claude"] = starbridge.claude.Application.info()
    data["env"] = _get_environment()
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


def _generate_mcp_server_config() -> dict:
    """Generate configuration file for Starbridge"""
    if _is_development_mode():
        return {
            "command": "uv",
            "args": [
                "--directory",
                _get_starbridge_path(),
                "run",
                "starbridge",
            ],
            "env": _get_environment(),
        }

    # Prompt for STARBRIDGE_ environment variables
    starbridge_path = pathlib.Path(_get_starbridge_path())
    env_example_path = starbridge_path / ".env.example"

    if not env_example_path.exists():
        return {"command": "uvx", "args": ["starbridge"], "env": {}}

    example_values = dotenv_values(env_example_path)
    env_values = {}

    for key, default in example_values.items():
        if key.startswith("STARBRIDGE_"):
            value = Prompt.ask(
                f"Enter value for {key}",
                default=default if default else None,
                password="TOKEN" in key or "SECRET" in key,
            )
            env_values[key] = value

    return {
        "command": "uvx",
        "args": ["starbridge"],
        "env": env_values,
    }


@cli.command()
def install(restart_claude: bool = True):
    """Install starbridge within Claude Desktop application by adding to configuration and restarting Claude Desktop app"""
    if starbridge.claude.Application.install_mcp_server(
        "starbridge",
        _generate_mcp_server_config(),
        restart_claude,
    ):
        console.print("Starbridge installed successfully")
    else:
        console.print("Starbridge was already installed", style="warning")


@cli.command()
def uninstall():
    """Install starbridge from Claude Desktop application by removing from configuration and restarting Claude Desktop app"""
    if starbridge.claude.Application.uninstall_mcp_server("starbridge"):
        console.print("Starbridge uninstalled successfully")
    else:
        console.print("Starbridge was no installed", style="warning")


@cli.command()
def health():
    """Health of starbridge and dependencie"""
    dependencies = {
        "confluence": starbridge.confluence.Service().health(),
        "claude": starbridge.claude.Application.health(),
    }
    healthy = all(status == "UP" for status in dependencies.values())
    console.print({"healthy": healthy, "dependencies": dependencies})


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
