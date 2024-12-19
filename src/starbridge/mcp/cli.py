"""
CLI to interact with Confluence
"""

import os
import pathlib
import re
import subprocess
import webbrowser
from typing import Annotated

import typer

from starbridge.base import __project_name__
from starbridge.utils.console import console

from .server import MCPServer

cli = typer.Typer(no_args_is_help=True)


@cli.command()
def health():
    """Check health of the services and their dependencies."""
    console.print(MCPServer().health())


@cli.command()
def services():
    """Services exposed by modules"""
    console.print(MCPServer.services())


@cli.command()
def tools():
    """Tools exposed by modules"""
    console.print(MCPServer.tools())


@cli.command()
def tool(name: str):
    """Get tool by name"""
    console.print(MCPServer.tool(name))


@cli.command()
def resources():
    """Resources exposed by modules"""
    console.print(MCPServer.resources())


@cli.command()
def resource(uri: str):
    """Get resource by URI"""
    console.print(MCPServer.resource(uri))


@cli.command()
def prompts():
    """Prompts exposed by modules"""
    console.print(MCPServer.prompts())


@cli.command()
def resource_types():
    """Resource types exposed by modules"""
    console.print(MCPServer.resource_types())


@cli.command()
def serve(
    host: Annotated[
        str,
        typer.Option(
            help="Host to run the server on",
        ),
    ] = None,
    port: Annotated[
        int,
        typer.Option(
            help="Port to run the server on",
        ),
    ] = None,
    debug: Annotated[
        bool,
        typer.Option(
            help="Debug mode",
        ),
    ] = True,
):
    """Run MCP server."""
    MCPServer().serve(host, port, debug)


@cli.command()
def inspect():
    """Run inspector."""
    project_root = str(pathlib.Path(__file__).parent.parent.parent.parent)
    console.print(
        f"Starbridge project root: {project_root}\nStarbridge environment:\n{os.environ}"
    )
    process = subprocess.Popen(
        [
            "npx",
            "@modelcontextprotocol/inspector",
            "uv",
            "--directory",
            project_root,
            "run",
            __project_name__,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )

    url_pattern = r"MCP Inspector is up and running at (http://[^\s]+)"

    while True:
        line = process.stdout.readline()
        if not line:
            break
        print(line, end="")
        match = re.search(url_pattern, line)
        if match:
            url = match.group(1)
            webbrowser.open(url)

    process.wait()
