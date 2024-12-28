import sys
from typing import Annotated, Any

import typer

from starbridge import (
    __is_development_mode__,
    __project_path__,
    __version__,
)
from starbridge.claude import Service as ClaudeService
from starbridge.claude import generate_mcp_server_config
from starbridge.mcp import MCPServer
from starbridge.utils import (
    console,
    get_logger,
    get_process_info,
    get_starbridge_env,
    prepare_cli,
    prompt_for_env,
)

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
    env: Annotated[
        list[str] | None,
        typer.Option(
            "--env",
            help='Environment variables in key=value format. Can be used multiple times in one call. Only STARBRIDGE_ prefixed vars are evaluated. Example --env STARBRIDGE_ATLASSIAN_URL="https://your-domain.atlassian.net" --env STARBRIDGE_ATLASSIAN_EMAIL="YOUR_EMAIL"',
        ),
    ] = None,
):
    """Run MCP Server - alias for 'mcp serve'"""
    # --env parsed in main __init__.py
    if ctx.invoked_subcommand is None:
        MCPServer.serve(host, port, debug)


@cli.command()
def health(json: Annotated[bool, typer.Option(help="Output health as JSON")] = False):
    """Check health of services and their dependencies."""
    health = MCPServer().health()
    if not health.healthy:
        logger.warning(f"health: {health}")
    if json:
        console.print(health.model_dump_json())
    else:
        console.print(health)


@cli.command()
def info():
    """Info about Starbridge and it's environment"""
    data: dict[str, Any] = {
        "version": __version__,
        "path": __project_path__,
        "development_mode": __is_development_mode__,
        "env": get_starbridge_env(),
        "process": get_process_info().model_dump(),
    }

    # Auto-discover and get info from all services
    for service_class in MCPServer.service_classes():
        service = service_class()
        service_name = service.__class__.__module__.split(".")[1]
        data[service_name] = service.info()

    console.print(data)
    logger.debug(data)


@cli.command()
def create_dot_env():
    """Create .env file for Starbridge. You will be prompted for settings."""
    if not __is_development_mode__:
        raise RuntimeError("This command is only available in development mode")

    with open(".env", "w") as f:
        for key, value in iter(prompt_for_env().items()):
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
):
    """Install starbridge within Claude Desktop application by adding to configuration and restarting Claude Desktop app"""
    if ClaudeService.install_mcp_server(
        generate_mcp_server_config(prompt_for_env(), image),
        restart=restart_claude,
    ):
        console.print("Starbridge installed with Claude Desktop application.")
        if not restart_claude:
            console.print(
                "Please restart Claude Desktop application to complete the installation."
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
):
    """Install starbridge from Claude Desktop application by removing from configuration and restarting Claude Desktop app"""
    if ClaudeService.uninstall_mcp_server(restart=restart_claude):
        console.print("Starbridge uninstalled from Claude Destkop application.")
    else:
        console.print("Starbridge was no installed", style="warning")


prepare_cli(cli, f"⭐ Starbridge v{__version__} - built with love in Berlin 🐻")

if __name__ == "__main__":
    try:
        cli()
    except Exception as e:
        logger.critical(f"Fatal error occurred: {e}")
        console.print(f"Fatal error occurred: {e}", style="error")
        sys.exit(1)
