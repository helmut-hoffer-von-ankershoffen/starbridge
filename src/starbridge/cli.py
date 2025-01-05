"""Command-line interface module for Starbridge, providing various commands for service management and configuration."""

import sys
from pathlib import Path
from typing import Annotated

import typer

from starbridge import (
    __is_development_mode__,
    __version__,
)
from starbridge.claude import Service as ClaudeService
from starbridge.claude import generate_mcp_server_config
from starbridge.mcp import MCPServer
from starbridge.utils import (
    console,
    get_logger,
    prepare_cli,
    prompt_for_env,
)

from .service import Service

logger = get_logger(__name__)

cli = typer.Typer(
    name="Starbridge CLI",
)


@cli.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    host: Annotated[
        str | None,
        typer.Option(
            help="Host to run the server on",
        ),
    ] = None,
    port: Annotated[
        int | None,
        typer.Option(
            help="Port to run the server on",
        ),
    ] = None,
    debug: Annotated[
        bool,
        typer.Option(
            help="Debug mode",
        ),
    ] = True,
    env: Annotated[  # noqa: ARG001
        list[str] | None,
        typer.Option(
            "--env",
            help=(
                "Environment variables in key=value format. Can be used multiple times in one call. "
                "Only STARBRIDGE_ prefixed vars are evaluated. Example --env "
                'STARBRIDGE_ATLASSIAN_URL="https://your-domain.atlassian.net" --env '
                'STARBRIDGE_ATLASSIAN_EMAIL="YOUR_EMAIL"'
            ),
        ),
    ] = None,
) -> None:
    """
    Run MCP Server - alias for 'mcp serve'.

    Args:
        ctx (typer.Context): Typer context
        host (str): Host to run the server on
        port (int): Port to run the server on
        debug (bool): Debug mode
        env (list[str]): Environment variables in key=value format. Can be used multiple times in one call.
            Only STARBRIDGE_ prefixed vars are used. Example --env
            'STARBRIDGE_ATLASSIAN_URL="https://your-domain.atlassian.net" --env STARBRIDGE_ATLASSIAN_EMAIL="YOUR_EMAIL"'

    """
    # --env parsed in main __init__.py
    if ctx.invoked_subcommand is None:
        MCPServer.serve(host, port, debug)


@cli.command()
def health(json: Annotated[bool, typer.Option(help="Output health as JSON")] = False) -> None:
    """Check health of services and their dependencies."""
    health = MCPServer().health()
    if not health.healthy:
        logger.warning("health: %s", health)
    if json:
        console.print(health.model_dump_json())
    else:
        console.print(health)


@cli.command()
def info() -> None:
    """Info about Starbridge and it's environment."""
    data = Service().info()
    console.print_json(data=data)
    logger.debug(data)


@cli.command()
def create_dot_env() -> None:
    """
    Create .env file for Starbridge. You will be prompted for settings.

    Raises:
        RuntimeError: If not running in development mode.

    """
    if not __is_development_mode__:
        msg = "This command is only available in development mode"
        raise RuntimeError(msg)
    with Path(".env").open("w", encoding="utf-8") as f:
        for key, value in iter(prompt_for_env().items()):
            f.write(f"{key}={value}\n")
            f.write(f"{key}={value}\n")


@cli.command()
def install(
    restart_claude: Annotated[
        bool,
        typer.Option(
            help="Restart Claude Desktop application post installation",
        ),
    ] = ClaudeService.platform_supports_restart(),
    image: Annotated[
        str,
        typer.Option(
            help="Docker image to use for Starbridge. Only applies if started as container.",
        ),
    ] = "helmuthva/starbridge:latest",
) -> None:
    """
    Install starbridge within Claude Desktop application.

    Adds starbridge configuration and restarts Claude Desktop app.

    Args:
        restart_claude (bool): Restart Claude Desktop application post installation
        image (str): Docker image to use for Starbridge. Only applies if started as container

    """
    if ClaudeService.install_mcp_server(
        generate_mcp_server_config(prompt_for_env(), image),
        restart=restart_claude,
    ):
        console.print("Starbridge installed with Claude Desktop application.")
        if not restart_claude:
            console.print(
                "Please restart Claude Desktop application to complete the installation.",
            )
    else:
        console.print("Starbridge was already installed", style="warning")


@cli.command()
def uninstall(
    restart_claude: Annotated[
        bool,
        typer.Option(
            help="Restart Claude Desktop application post installation",
        ),
    ] = ClaudeService.platform_supports_restart(),
) -> None:
    """
    Uninstall starbridge from Claude Desktop application.

    Removes starbridge configuration and restarts Claude Desktop app.

    Args:
        restart_claude (bool): Restart Claude Desktop application post installation

    """
    if ClaudeService.uninstall_mcp_server(restart=restart_claude):
        console.print("Starbridge uninstalled from Claude Destkop application.")
    else:
        console.print("Starbridge was no installed", style="warning")


prepare_cli(cli, f"⭐ Starbridge v{__version__} - built with love in Berlin 🐻")

if __name__ == "__main__":
    try:
        cli()
    except Exception as e:  # noqa: BLE001
        logger.critical("Fatal error occurred: %s", e)
        console.print(f"Fatal error occurred: {e}", style="error")
        sys.exit(1)
