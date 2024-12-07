"""
CLI to interact with Confluence
"""

import asyncio
import os
import pathlib
import subprocess

import typer

from starbridge.utils.console import console

from .server import MCPServer, mcp_server

cli = typer.Typer(no_args_is_help=True)


@cli.command()
def tools():
    """Tools exposed by modules"""
    server = MCPServer()
    # FIXME
    console.print(server.tool_list())


@cli.command()
def inspect():
    """Run inspector."""
    project_root = str(pathlib.Path(__file__).parent.parent.parent.parent)
    console.print("Starbridge project root:", project_root)
    console.print("Starbridge environment:")
    console.print(os.environ)
    subprocess.run(
        [
            "npx",
            "@modelcontextprotocol/inspector",
            "uv",
            "--directory",
            project_root,
            "run",
            "starbridge",
        ],
        check=True,
    )


@cli.command()
def serve():
    """Run MCP server."""
    asyncio.run(mcp_server())
