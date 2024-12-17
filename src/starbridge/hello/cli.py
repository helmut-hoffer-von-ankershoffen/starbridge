"""
CLI to interact with Hello World
"""

import typer

from starbridge.utils.console import console

from .service import Service

cli = typer.Typer(no_args_is_help=True)


@cli.command(name="info")
def info():
    """Info about Hello World"""
    console.print(Service().info())


@cli.command(name="world")
def world():
    """Print Hello World!"""
    console.print(Service().hello())
