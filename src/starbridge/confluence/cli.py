"""
CLI to interact with Confluence
"""

import typer
from pydantic import AnyUrl

from ..utils.console import console
from .handler import Handler

cli = typer.Typer(no_args_is_help=True)


@cli.command(name="info")
def info(
    ctx: typer.Context,
    verbose: bool = False,
):  # pylint: disable=W0613
    """Info about Confluence"""
    console.print(Handler().info())


cli_mcp = typer.Typer(no_args_is_help=True)
cli.add_typer(cli_mcp, name="mcp")


@cli_mcp.callback()
def mcp(ctx: typer.Context, verbose: bool = False):  # pylint: disable=W0613
    """MCP endpoints"""


@cli_mcp.command(name="tools")
def tool_list(
    ctx: typer.Context,
    verbose: bool = False,
):  # pylint: disable=W0613
    """List tools exposed via MCP"""
    console.print(Handler.tool_list())


@cli_mcp.command(name="resources")
def resources_list(
    ctx: typer.Context,
    verbose: bool = False,
):  # pylint: disable=W0613
    """List resources exposed via MCP"""
    console.print(Handler().resource_list())


@cli_mcp.command(name="resource")
def resource_get(
    ctx: typer.Context,
    verbose: bool = False,
    uri: str = typer.Option(..., help="Resource URI"),
):  # pylint: disable=W0613
    """Get resource exposed via MCP"""
    console.print(Handler().resource_get(uri=AnyUrl(uri)))


@cli_mcp.command(name="prompts")
def prompt_list(
    ctx: typer.Context,
    verbose: bool = False,
):  # pylint: disable=W0613
    """List prompts exposed via MCP"""
    console.print(Handler().prompt_list())


@cli_mcp.command(name="space-summary")
def prompt_space_summary(
    ctx: typer.Context,
    verbose: bool = False,
):  # pylint: disable=W0613
    """Summary of all spaces"""
    console.print(Handler().mcp_prompt_starbridge_space_summary())


cli_space = typer.Typer(no_args_is_help=True)
cli.add_typer(cli_space, name="space")


@cli_space.callback()
def space(ctx: typer.Context, verbose: bool = False):  # pylint: disable=W0613
    """Operations on Confluence spaces"""


@cli_space.command(name="list")
def space_list(
    ctx: typer.Context,
    verbose: bool = False,
):  # pylint: disable=W0613
    """Get info about all space"""
    console.print(Handler().space_list())


cli_page = typer.Typer(no_args_is_help=True)
cli.add_typer(cli_page, name="page")


@cli_page.callback()
def page(ctx: typer.Context, verbose: bool = False):  # pylint: disable=W0613
    """Operations on Confluence pages"""


@cli_page.command(name="create")
def page_list(
    ctx: typer.Context,
    verbose: bool = False,
    space_key: str = typer.Option(..., help="Space key"),
    title: str = typer.Option(..., help="Title of the page"),
    body: str = typer.Option(..., help="Body of the page"),
    page_id: str = typer.Option(None, help="Parent page id"),
):  # pylint: disable=W0613
    """Create a new page"""
    console.print(Handler().page_create(space_key, title, body, page_id))
