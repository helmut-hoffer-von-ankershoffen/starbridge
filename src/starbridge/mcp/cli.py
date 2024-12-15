"""
CLI to interact with Confluence
"""

import asyncio
import os
import pathlib
import subprocess

import typer

from starbridge.utils.console import console

from .server import MCPServer, mcp_run_coroutine

cli = typer.Typer(no_args_is_help=True)


@cli.command()
def tools():
    """Tools exposed by modules"""
    server = MCPServer()
    console.print(asyncio.run(server.tool_list()))


@cli.command()
def inspect():
    """Run inspector."""
    project_root = str(pathlib.Path(__file__).parent.parent.parent.parent)
    console.print(
        f"Starbridge project root: {project_root}\nStarbridge environment:\n{os.environ}"
    )
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
    asyncio.run(mcp_run_coroutine())
