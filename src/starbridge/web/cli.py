"""
CLI to interact with the world wide web
"""

import asyncio
import json
import sys
from typing import Annotated

import typer
from requests.exceptions import RequestException
from rich.panel import Panel
from rich.text import Text

from starbridge.utils.console import console

from .service import Service
from .types import Format, RobotForbiddenException

cli = typer.Typer(name="web", help="Web operations")


@cli.command()
def health():
    """Health of the web module"""
    console.print_json(Service().health().model_dump_json())


@cli.command()
def info():
    """Info about the web module"""
    console.print(Service().info())


@cli.command()
def get(
    url: Annotated[str, typer.Argument(help="URL to fetch")],
    format: Annotated[
        Format,
        typer.Option(help="format to convert the content to", case_sensitive=False),
    ] = Format.markdown,
    accept_language: Annotated[
        str,
        typer.Option(
            help="Accept-Language header value to send in the request",
        ),
    ] = "en-US,en;q=0.9,de;q=0.8",
    additional_context: Annotated[
        bool,
        typer.Option(
            help="include additional context in the response",
        ),
    ] = True,
    llms_full_txt: Annotated[
        bool,
        typer.Option(
            help="provide llms-full.txt in contexts",
        ),
    ] = False,
) -> None:
    """Fetch content from the world wide web via HTTP GET."""
    try:
        rtn = asyncio.run(
            Service().get(
                url=url,
                format=format,
                accept_language=accept_language,
                additional_context=additional_context,
                llms_full_txt=llms_full_txt,
            )
        )
        if format is Format.bytes:
            console.print(rtn)
        else:
            console.print_json(json.dumps(rtn))
    except RequestException as e:
        text = Text()
        text.append(str(e))
        console.print(
            Panel(
                text,
                title="Request failed",
                border_style="red",
            )
        )
        sys.exit(1)
    except RobotForbiddenException as e:
        text = Text()
        text.append(str(e))
        console.print(
            Panel(
                text,
                title="robots.txt disallows crawling",
                border_style="red",
            )
        )
        sys.exit(1)
