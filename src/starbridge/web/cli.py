"""CLI to interact with the world wide web."""

import asyncio
import sys
from typing import Annotated

import typer
from requests.exceptions import RequestException
from rich.panel import Panel
from rich.text import Text

from starbridge.utils.console import console

from .models import RobotForbiddenError
from .service import Service

cli = typer.Typer(name="web", help="Web operations")


@cli.command()
def health() -> None:
    """Health of the web module."""
    console.print_json(Service().health().model_dump_json())


@cli.command()
def info() -> None:
    """Info about the web module."""
    console.print_json(data=Service().info())


@cli.command()
def get(  # noqa: PLR0913, PLR0917
    url: Annotated[str, typer.Argument(help="URL to fetch")],
    accept_language: Annotated[
        str,
        typer.Option(
            help="Accept-Language header value to send in the request",
        ),
    ] = "en-US,en;q=0.9,de;q=0.8",
    transform_to_markdown: Annotated[
        bool,
        typer.Option(
            help="if possible transform content to markdown",
        ),
    ] = True,
    extract_links: Annotated[
        bool,
        typer.Option(
            help="include extracted links in the response",
        ),
    ] = True,
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
    force_not_respecting_robots_txt: Annotated[
        bool,
        typer.Option(
            "--force-not-respecting-robots-txt",
            help="Force not respecting robots.txt. If True, the agent will ignore robots.txt."
            "If False, the agent will respect robots.txt if the environment variable"
            "STARBRIDGE_WEB_RESPPECT_ROBOTS_TXT is set to 1."
            "Defaults to False.",
        ),
    ] = False,
) -> None:
    """
    Fetch content from the world wide web via HTTP GET.

    Converts to content type as a best effort, extracts links, and provides additional context.

    Args:
        url (str): URL to fetch
        accept_language (str): Accept-Language header value to send in the request
        transform_to_markdown (bool): if possible transform content to markdown
        extract_links (bool): include extracted links in the response
        additional_context (bool): include additional context in the response
        llms_full_txt (bool): provide llms-full.txt in contexts
        force_not_respecting_robots_txt (bool): do not respect robots.txt
            If False, the agent will respect robots.txt if the environment variable
                STARBRIDGE_WEB_RESPPECT_ROBOTS_TXT is set to 1.
            Defaults to False

    """
    try:
        rtn = asyncio.run(
            Service().get(
                url=url,
                accept_language=accept_language,
                transform_to_markdown=transform_to_markdown,
                extract_links=extract_links,
                additional_context=additional_context,
                llms_full_txt=llms_full_txt,
                force_not_respecting_robots_txt=force_not_respecting_robots_txt,
            ),
        )
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
    except RobotForbiddenError as e:
        text = Text()
        text.append(str(e))
        console.print(
            Panel(
                text,
                title="robots.txt disallows crawling",
                border_style="red",
            ),
        )
        sys.exit(1)
