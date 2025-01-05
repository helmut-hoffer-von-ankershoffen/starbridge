"""CLI to search."""

import asyncio
import sys
from typing import Annotated

import typer
from requests.exceptions import RequestException
from rich.panel import Panel
from rich.text import Text

from starbridge.utils.console import console

from .service import Service

cli = typer.Typer(name="search", help="Search operations")


@cli.command()
def health() -> None:
    """Health of the search module."""
    console.print_json(Service().health().model_dump_json())


@cli.command()
def info() -> None:
    """Info about the search module."""
    console.print_json(data=Service().info())


@cli.command()
def web(
    q: Annotated[str, typer.Argument(help="Query")],
) -> None:
    """
    Search the web.

    Args:
        q (str): Query

    """
    try:
        rtn = asyncio.run(Service().web(q=q))
        console.print_json(rtn.model_dump_json())
    except RequestException as e:
        text = Text()
        text.append(str(e))
        console.print(
            Panel(
                text,
                title="Request failed",
                border_style="red",
            ),
        )
        sys.exit(1)
