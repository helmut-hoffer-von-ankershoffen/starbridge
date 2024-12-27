"""
CLI to interact with Confluence
"""

import json
from typing import Annotated

import typer

from starbridge.utils.console import console

from .service import Service

cli = typer.Typer(name="confluence", help="Confluence operations")


@cli.command()
def health():
    """Health of Confluence"""
    console.print(Service().health().model_dump_json())


@cli.command()
def info():
    """Info about Confluence"""
    console.print(Service().info())


cli_mcp = typer.Typer()
cli.add_typer(cli_mcp, name="mcp")


@cli_mcp.callback()
def mcp():
    """MCP endpoints"""


@cli_mcp.command()
def tools():
    """List tools exposed via MCP"""
    console.print(Service().tool_list())


@cli_mcp.command()
def resources():
    """List resources exposed via MCP"""
    console.print(Service().resource_list())


@cli_mcp.command()
def resource_types():
    """List resources exposed via MCP"""
    console.print(Service().resource_type_list())


@cli_mcp.command(name="space")
def resource_space(
    key: Annotated[
        str, typer.Argument(help="Key of the space to retrieve as resource")
    ],
):
    """Get space resource as exposed via MCP"""
    console.print(Service().space_get(key))


@cli_mcp.command()
def prompts():
    """List prompts exposed via MCP"""
    console.print(Service().prompt_list())


@cli_mcp.command(name="space-summary")
def prompt_space_summary(
    style: Annotated[str, typer.Option(help="Style of summary")] = "brief",
):
    """Prompt to generate summary of spaces"""
    console.print(Service().space_summary(style))


cli_space = typer.Typer()
cli.add_typer(cli_space, name="space")


@cli_space.callback()
def space():
    """Operations on Confluence spaces"""


@cli_space.command(name="list")
def space_list():
    """Get info about all space"""
    console.print_json(json.dumps(Service().space_list()))


cli_page = typer.Typer()
cli.add_typer(cli_page, name="page")


@cli_page.callback()
def page():
    """Operations on Confluence pages"""


@cli_page.command(name="list")
def page_list(space_key: str = typer.Option(..., help="Space key")):
    """List pages in a space"""
    console.print(Service().page_list(space_key))


@cli_page.command(name="create")
def page_create(
    space_key: str = typer.Option(..., help="Space key"),
    title: str = typer.Option(..., help="Title of the page"),
    body: str = typer.Option(..., help="Body of the page"),
    page_id: str = typer.Option(None, help="Parent page id"),
):
    """Create a new page"""
    console.print(Service().page_create(space_key, title, body, page_id))


@cli_page.command(name="read")
def page_get(
    page_id: str = typer.Option(None, help="Page id"),
):
    """Read a page"""
    console.print(Service().page_get(page_id))


@cli_page.command(name="update")
def page_update(
    page_id: str = typer.Option(..., help="Pager id"),
    title: str = typer.Option(..., help="Title of the page"),
    body: str = typer.Option(..., help="Body of the page"),
):
    """Update a page"""
    console.print(Service().page_update(page_id, title, body))


@cli_page.command(name="delete")
def page_delete(page_id: str = typer.Option(..., help="Pager id")):
    """Delete a page"""
    console.print(Service().page_delete(page_id))
