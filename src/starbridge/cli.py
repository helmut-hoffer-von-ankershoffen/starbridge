import importlib.metadata

import typer
from dotenv import load_dotenv

import starbridge.confluence
import starbridge.mcp

from .utils.console import console

load_dotenv()

__version__ = importlib.metadata.version("starbridge")

cli = typer.Typer(
    name="Starbridge CLI",
    no_args_is_help=True,
    help=f"Starbride (Version: {__version__})",
    epilog="Built with love in Berlin by Helmut Hoffer von Ankershoffen",
)


@cli.command()
def info():
    """Info about Starbridge Environment"""
    console.print({"version": __version__})


@cli.command()
def health():
    """Health of starbridge and dependencie"""
    console.print({"health": "OK"})


cli.add_typer(
    starbridge.mcp.cli,
    name="mcp",
    help="MCP operations",
)
cli.add_typer(
    starbridge.confluence.cli, name="confluence", help="Confluence operations"
)


if __name__ == "__main__":
    cli()
