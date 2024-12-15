"""
CLI to interact with Confluence
"""

import typer
from pydantic import AnyUrl

from starbridge.utils.console import console

from .service import Service

cli = typer.Typer(no_args_is_help=True)


@cli.command(name="info")
def info():
    """Info about Confluence"""
    console.print(Service().info())


cli_mcp = typer.Typer(no_args_is_help=True)
cli.add_typer(cli_mcp, name="mcp")


@cli_mcp.callback()
def mcp():
    """MCP endpoints"""


@cli_mcp.command(name="tools")
def tool_list():
    """List tools exposed via MCP"""
    console.print(Service().tool_list())


@cli_mcp.command(name="resources")
def resources_list():
    """List resources exposed via MCP"""
    console.print(Service().resource_list())


@cli_mcp.command(name="resource")
def resource_get(
    uri: str = typer.Option(..., help="Resource URI"),
):
    """Get resource exposed via MCP"""
    console.print(Service().resource_get(uri=AnyUrl(uri)))


@cli_mcp.command(name="prompts")
def prompt_list():
    """List prompts exposed via MCP"""
    console.print(Service().prompt_list())


@cli_mcp.command(name="space-summary")
def prompt_space_summary():
    """Summary of all spaces"""
    console.print(Service().mcp_prompt_starbridge_space_summary())


cli_space = typer.Typer(no_args_is_help=True)
cli.add_typer(cli_space, name="space")


@cli_space.callback()
def space():
    """Operations on Confluence spaces"""


@cli_space.command(name="list")
def space_list():
    """Get info about all space"""
    console.print(Service().space_list())


cli_page = typer.Typer(no_args_is_help=True)
cli.add_typer(cli_page, name="page")


@cli_page.callback()
def page():
    """Operations on Confluence pages"""


@cli_page.command(name="create")
def page_list(
    space_key: str = typer.Option(..., help="Space key"),
    title: str = typer.Option(..., help="Title of the page"),
    body: str = typer.Option(..., help="Body of the page"),
    page_id: str = typer.Option(None, help="Parent page id"),
):
    """Create a new page"""
    console.print(Service().page_create(space_key, title, body, page_id))
