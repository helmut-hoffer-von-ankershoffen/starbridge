"""
CLI to interact with Claude Desktop application
"""

import typer

from ..utils.console import console
from .application import Application

cli = typer.Typer(no_args_is_help=True)


@cli.command(name="config")
def config():
    """Print config of Claude Desktop application"""
    if Application.is_installed() is False:
        console.print(
            "Claude Desktop application is not installed at '{Application.application_path()'}"
        )
        return
    if Application.config_path().is_file() is False:
        console.print("No config file found at '{Application.config_path()}'")
        return
    console.print(f"Printing config file at '{Application.config_path()}'")
    console.print_json(data=Application.config_read())


@cli.command(name="restart")
def restart():
    """Restart Claude Desktop application"""
    Application.restart()
    console.print("Claude Desktop application was restarted")
