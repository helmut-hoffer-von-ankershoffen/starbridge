"""
CLI to interact with Claude Desktop application
"""

import pathlib
import subprocess
from typing import Annotated

import typer

from ..utils.console import console
from .application import Application

cli = typer.Typer(no_args_is_help=True)


@cli.command(name="config")
def config():
    """Print config of Claude Desktop application"""
    if Application.is_installed() is False:
        console.print(
            "Claude Desktop application is not installed at '{Application.application_path()'} - you can install it from https://claude.ai/download"
        )
        return
    if Application.config_path().is_file() is False:
        console.print("No config file found at '{Application.config_path()}'")
        return
    console.print(f"Printing config file at '{Application.config_path()}'")
    console.print_json(data=Application.config_read())


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
    log_path = Application.log_path(name if name != "main" else None)
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
                Application.log_path(name if name != "main" else None),
            ],
            check=False,
        )
    else:
        subprocess.run(
            [
                "tail",
                "-n",
                str(last),
                Application.log_path(name if name != "main" else None),
            ],
            check=False,
        )


@cli.command(name="restart")
def restart():
    """Restart Claude Desktop application"""
    if Application.is_installed() is False:
        console.print(
            "Claude Desktop application is not installed at '{Application.application_path()'} - you can install it from https://claude.ai/download"
        )
        return
    Application.restart()
    console.print("Claude Desktop application was restarted")
