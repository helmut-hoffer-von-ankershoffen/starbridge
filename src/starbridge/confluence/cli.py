"""CLI to interact with Confluence."""

from typing import Annotated

import typer

from starbridge.utils.console import console

from .service import Service

cli = typer.Typer(name="confluence", help="Confluence operations")


@cli.command()
def health() -> None:
    """Health of Confluence."""
    console.print_json(Service().health().model_dump_json())


@cli.command()
def info() -> None:
    """Info about Confluence."""
    console.print_json(data=Service().info())


cli_mcp = typer.Typer()
cli.add_typer(cli_mcp, name="mcp")


@cli_mcp.callback()
def mcp() -> None:
    """MCP endpoints."""


@cli_mcp.command()
def tools() -> None:
    """List tools exposed via MCP."""
    console.print(Service().tool_list())


@cli_mcp.command()
def resources() -> None:
    """List resources exposed via MCP."""
    console.print(Service().resource_list())


@cli_mcp.command()
def resource_types() -> None:
    """List resources exposed via MCP."""
    console.print(Service().resource_type_list())


@cli_mcp.command(name="space")
def resource_space(
    key: Annotated[
        str,
        typer.Argument(help="Key of the space to retrieve as resource"),
    ],
) -> None:
    """Get space resource as exposed via MCP."""
    console.print(Service().space_get(key))


@cli_mcp.command()
def prompts() -> None:
    """List prompts exposed via MCP."""
    console.print(Service().prompt_list())


@cli_mcp.command(name="space-summary")
def prompt_space_summary(
    style: Annotated[str, typer.Option(help="Style of summary")] = "brief",
) -> None:
    """
    Prompt to generate summary of spaces.

    Args:
        style (str): Style of summary

    """
    console.print(Service().space_summary(style))


cli_space = typer.Typer()
cli.add_typer(cli_space, name="space")


@cli_space.callback()
def space() -> None:
    """Operations on Confluence spaces."""


@cli_space.command(name="list")
def space_list() -> None:
    """Get info about all space."""
    console.print_json(data=Service().space_list())


cli_page = typer.Typer()
cli.add_typer(cli_page, name="page")


@cli_page.callback()
def page() -> None:
    """Operations on Confluence pages."""


@cli_page.command(name="list")
def page_list(space_key: str = typer.Option(..., help="Space key")) -> None:
    """
    List pages in a space.

    Args:
        space_key (str): Key of the space to list pages from

    """
    console.print(Service().page_list(space_key))


@cli_page.command(name="search")
def page_search(
    query: str = typer.Option(..., help="Confluence query language (CQL) query to search for pages"),
) -> None:
    """
    Search pages in a space.

    Args:
        query (str): Confluence query language (CQL) query to search for pages

    """
    console.print(Service().page_search(query))


@cli_page.command(name="create")
def page_create(
    space_key: str = typer.Option(..., help="Space key"),
    title: str = typer.Option(..., help="Title of the page"),
    body: str = typer.Option(..., help="Body of the page"),
    page_id: str = typer.Option(None, help="Parent page id"),
) -> None:
    """
    Create a new page.

    Args:
        space_key (str): Key of the space to create the page in
        title (str): Title of the page
        body (str): Body of the page
        page_id (str): Parent page

    """
    console.print(Service().page_create(space_key, title, body, page_id))


@cli_page.command(name="read")
def page_get(
    page_id: str = typer.Option(None, help="Page id"),
) -> None:
    """Read a page."""
    console.print(Service().page_get(page_id))


@cli_page.command(name="update")
def page_update(
    page_id: str = typer.Option(..., help="Pager id"),
    title: str = typer.Option(..., help="Title of the page"),
    body: str = typer.Option(..., help="Body of the page"),
) -> None:
    """
    Update a page.

    Args:
        page_id (str): Page id
        title (str): Title of the page
        body (str): Body of the page

    """
    console.print(Service().page_update(page_id, title, body))


@cli_page.command(name="delete")
def page_delete(page_id: str = typer.Option(..., help="Pager id")) -> None:
    """
    Delete a page.

    Args:
        page_id (str): Page id

    """
    console.print(Service().page_delete(page_id))
