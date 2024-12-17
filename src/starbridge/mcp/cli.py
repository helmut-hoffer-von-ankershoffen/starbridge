"""
CLI to interact with Confluence
"""

import asyncio
import os
import pathlib
import re
import subprocess
import webbrowser

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
    process = subprocess.Popen(
        [
            "npx",
            "@modelcontextprotocol/inspector",
            "uv",
            "--directory",
            project_root,
            "run",
            "starbridge",
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


@cli.command()
def serve():
    """Run MCP server."""
    asyncio.run(mcp_run_coroutine())
