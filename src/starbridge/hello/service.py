"""Handles Confluence operations."""

import json

import mcp.types as types
import typer

from starbridge.mcp import MCPBaseService, MCPContext
from starbridge.mcp.decorators import mcp_tool

from . import cli


class Service(MCPBaseService):
    """Service class for Hello World operations."""

    @classmethod
    def get_cli(cls) -> tuple[str | None, typer.Typer | None]:
        """Get CLI for Hello World service."""
        return "hello", cli.cli

    def __init__(self):
        pass

    def info(self) -> dict:
        return {"locale": "en_US"}

    @mcp_tool()
    def starbridge_hello_info(self, context: MCPContext):
        """Info about Hello world environment"""
        return [types.TextContent(type="text", text=json.dumps(self.info(), indent=2))]

    def health(self) -> str:
        return "UP"

    def hello(self) -> str:
        return "Hello, World!"

    @mcp_tool()
    def starbridge_hello_hello(self, context: MCPContext | None = None):
        """Print hello world!"""
        return [types.TextContent(type="text", text=self.hello())]
