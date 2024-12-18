"""
CLI to interact with Claude Desktop application
"""

import pathlib
import subprocess
from typing import Annotated

import typer

from starbridge.utils.console import console

from .service import Service

cli = typer.Typer(no_args_is_help=True)
service = Service()


@cli.command()
def health():
    """Health of Claude"""
    console.print(Service().health())


@cli.command()
def info():
    """Info about Claude"""
    console.print(Service().info())


@cli.command()
def config():
    """Print config of Claude Desktop application"""
    if not service.is_installed():
        console.print(
            f"Claude Desktop application is not installed at '{service.application_directory()}' - you can install it from https://claude.ai/download"
        )
        return
    if not service.config_path().is_file():
        console.print(f"No config file found at '{service.config_path()}'")
        return
    console.print(f"Printing config file at '{service.config_path()}'")
    console.print_json(data=service.config_read())


@cli.command()
def log(
    tail: Annotated[
        bool,
        typer.Option(
            help="Tail logs",
        ),
    ] = False,
    last: Annotated[
        int,
        typer.Option(help="Number of lines to show"),
    ] = 100,
    name: Annotated[
        str,
        typer.Option(
            help="Name of the MCP server - use 'main' for main mcp.log of Claude Desktop application",
        ),
    ] = "starbridge",
):
    """Show logs."""
    log_path = service.log_path(name if name != "main" else None)
    size = pathlib.Path(log_path).stat().st_size
    human_size = (
        f"{size / 1024 / 1024:.1f}MB" if size > 1024 * 1024 else f"{size / 1024:.1f}KB"
    )
    console.print(
        f"Showing max {last} lines of log at '{log_path}' ({human_size}{', tailing' if tail else ''})",
    )
    if tail:
        subprocess.run(
            [
                "tail",
                "-n",
                str(last),
                "-f",
                service.log_path(name if name != "main" else None),
            ],
            check=False,
        )
    else:
        subprocess.run(
            [
                "tail",
                "-n",
                str(last),
                service.log_path(name if name != "main" else None),
            ],
            check=False,
        )


@cli.command(name="restart")
def restart():
    """Restart Claude Desktop application"""
    if not service.is_installed():
        console.print(
            f"Claude Desktop application is not installed at '{service.application_directory()}' - you can install it from https://claude.ai/download"
        )
        return
    service.restart()
    console.print("Claude Desktop application was restarted")
