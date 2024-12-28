"""
CLI to interact with Claude Desktop application
"""

import pathlib
import subprocess
from typing import Annotated

import typer

from starbridge import __project_name__
from starbridge.utils.console import console

from .service import Service

cli = typer.Typer(name="claude", help="Claude Desktop application operations")


@cli.command()
def health():
    """Health of Claude"""
    console.print(Service().health().model_dump_json())


@cli.command()
def info():
    """Info about Claude"""
    console.print(Service().info())


@cli.command()
def config():
    """Print config of Claude Desktop application"""
    if not Service.is_installed():
        console.print(
            f"Claude Desktop application is not installed at '{Service.application_directory()}' - you can install it from https://claude.ai/download"
        )
        return
    if not Service.config_path().is_file():
        console.print(f"No config file found at '{Service.config_path()}'")
        return
    console.print(f"Printing config file at '{Service.config_path()}'")
    console.print_json(data=Service.config_read())


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
    ] = __project_name__,
):
    """Show logs."""
    log_path = Service.log_path(name if name != "main" else None)
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
                str(Service.log_path(name if name != "main" else None)),
            ],
            check=False,
        )
    else:
        subprocess.run(
            [
                "tail",
                "-n",
                str(last),
                str(Service.log_path(name if name != "main" else None)),
            ],
            check=False,
        )


@cli.command(name="restart")
def restart():
    """Restart Claude Desktop application"""
    if not Service.is_installed():
        console.print(
            f"Claude Desktop application is not installed at '{Service.application_directory()}' - you can install it from https://claude.ai/download"
        )
        return
    Service().restart()
    console.print("Claude Desktop application was restarted")
