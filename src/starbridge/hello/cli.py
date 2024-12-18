"""
CLI to interact with Hello World
"""

import typer

from starbridge.utils.console import console

from .service import Service

cli = typer.Typer(no_args_is_help=True)


@cli.command()
def health():
    """Health of Hello World"""
    console.print(Service().health())


@cli.command()
def info():
    """Info about Hello World"""
    console.print(Service().info())


@cli.command()
def hello():
    """Print Hello World!"""
    console.print(Service().hello())


@cli.command()
def bridge():
    """Show image of starbridge"""
    console.print(Service().bridge())
