"""
CLI to interact with Confluence
"""

import os
import re
import subprocess
import webbrowser
from typing import Annotated

import typer

from starbridge import __project_name__, __version__
from starbridge.utils import console, get_process_info

from .server import MCPServer

cli = typer.Typer(name="mcp", help="MCP operations")


@cli.command()
def health():
    """Check health of the services and their dependencies."""
    console.print(MCPServer().health().model_dump_json())


@cli.command()
def services():
    """Services exposed by modules"""
    console.print(MCPServer.service_classes())


@cli.command()
def tools():
    """Tools exposed by modules"""
    console.print(MCPServer.tools())


@cli.command()
def tool(
    name: str,
    arguments: Annotated[
        list[str] | None, typer.Option(help="Arguments in key=value format")
    ] = None,
):
    """Get tool by name with optional arguments"""
    args = {}
    if arguments:
        for arg in arguments:
            key, value = arg.split("=", 1)
            args[key] = value
    console.print(MCPServer.tool(name, args))


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
    env: Annotated[  # Parsed in bootstrap.py
        list[str] | None,
        typer.Option(
            "--env",
            help='Environment variables in key=value format. Can be used multiple times in one call. Only STARBRIDGE_ prefixed vars are used. Example --env STARBRIDGE_ATLASSIAN_URL="https://your-domain.atlassian.net" --env STARBRIDGE_ATLASSIAN_EMAIL="YOUR_EMAIL"',
        ),
    ] = None,
):
    """Run MCP server."""
    MCPServer().serve(host, port, debug)


@cli.command()
def inspect():
    """Run inspector."""
    process_info = get_process_info()
    console.print(
        f"⭐ Starbridge controller: v{__version__} (project root {process_info.project_root}, pid {process_info.pid}), parent '{process_info.parent.name}' (pid {process_info.parent.pid})"
    )
    env_args = []
    for key, value in os.environ.items():
        if key.startswith("STARBRIDGE_"):
            env_args.extend(["--env", f'{key}="{value}"'])
    cmd = [
        "npx",
        "@modelcontextprotocol/inspector",
        "uv",
        "--directory",
        process_info.project_root,
        "run",
        "--no-dev",
        __project_name__,
    ] + env_args
    console.print(f"Executing: {' '.join(cmd)}")

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=os.environ,
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
            console.print(f"Opened browser pointing to MCP Inspector at {url}")
            webbrowser.open(url)

    process.wait()
