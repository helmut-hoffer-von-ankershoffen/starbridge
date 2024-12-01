"""
CLI to interact with Confluence
"""

import asyncio
import os

import typer

from .server import run_server

cli = typer.Typer(no_args_is_help=True)


@cli.command()
def serve(
    confluence_url: str = typer.Option(
        ..., envvar="CONFLUENCE_URL", help="Confluence url"
    ),
    confluence_email_address: str = typer.Option(
        ..., envvar="CONFLUENCE_EMAIL_ADDRESS", help="Confluence email address"
    ),
    confluence_api_token: str = typer.Option(
        ..., envvar="CONFLUENCE_API_TOKEN", help="Confluence API token"
    ),
):
    """Run MCP server."""
    os.environ.setdefault("CONFLUENCE_URL", confluence_url)
    os.environ.setdefault("CONFLUENCE_EMAIL_ADDRESS", confluence_email_address)
    os.environ.setdefault("CONFLUENCE_API_TOKEN", confluence_api_token)
    asyncio.run(run_server())
