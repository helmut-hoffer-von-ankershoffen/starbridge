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

cli = typer.Typer()


@cli.command()
def health():
    """Check health of the services and their dependencies."""
    console.print(MCPServer().health().model_dump_json())


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
def prompt(
    name: str,
    arguments: Annotated[
        list[str] | None, typer.Option(help="Arguments in key=value format")
    ] = None,
):
    """Get a prompt by name with optional arguments"""
    args = {}
    if arguments:
        for arg in arguments:
            key, value = arg.split("=", 1)
            args[key] = value
    console.print(MCPServer.prompt(name, args))


@cli.command()
def resource_types():
    """Resource types exposed by modules"""
    console.print(MCPServer.resource_types())


@cli.command()
def serve(
    host: Annotated[
        str | None,
        typer.Option(
            help="Host to run the server on",
        ),
    ] = None,
    port: Annotated[
        int | None,
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
        text=True,
    )

    url_pattern = r"MCP Inspector is up and running at (http://[^\s]+)"

    while True:
        if process.stdout is not None:
            line = process.stdout.readline()
        else:
            line = ""
        if not line:
            break
        print(line, end="")
        match = re.search(url_pattern, line)
        if match:
            url = match.group(1)
            console.print(print(f"Opened browser pointing to MCP Inspector at {url}"))
            webbrowser.open(url)

    process.wait()
