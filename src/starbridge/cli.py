import asyncio
import importlib.metadata

import typer

from .server import run_server
from .utils.console import console

__version__ = importlib.metadata.version("starbridge")

cli = typer.Typer(
    name="Starbridge CLI",
    no_args_is_help=True,
    help=f"Starbride (Version: {__version__})",
    epilog="Built with love in Berlin by Helmut Hoffer von Ankershoffen",
)


@cli.command()
def serve():
    """Run MCP server."""
    asyncio.run(run_server())


@cli.command()
def info():
    """Info about Starbridge Environment"""
    console.print({"version": __version__})


@cli.command()
def health():
    """Health of starbridge and dependencie"""
    console.print({"health": "OK"})


if __name__ == "__main__":
    cli()
