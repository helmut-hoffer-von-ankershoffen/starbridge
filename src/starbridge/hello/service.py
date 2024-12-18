"""Handles Confluence operations."""

import io
import os

# TODO: Generic solution
os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = "/opt/homebrew/lib"

import cairosvg
import cairosvg.svg
import typer
from PIL import Image

from starbridge.mcp import MCPBaseService, MCPContext, mcp_tool

from . import cli


class Service(MCPBaseService):
    """Service class for Hello World operations."""

    def __init__(self):
        pass

    @staticmethod
    def get_cli() -> tuple[str | None, typer.Typer | None]:
        """Get CLI for Hello World service."""
        return "hello", cli.cli

    @mcp_tool()
    def health(self, context: MCPContext | None = None) -> str:
        return "UP"

    @mcp_tool()
    def info(self, context: MCPContext | None = None) -> dict:
        """Info about Hello world environment"""
        return {"locale": "en_US"}

    @mcp_tool()
    def hello(self, context: MCPContext | None = None):
        """Print hello world!"""
        context.error("Hello world!")
        return self.hello()

    @mcp_tool()
    def bridge(self, context: MCPContext | None = None):
        """Show image of starbridge"""
        return Image.open(
            io.BytesIO(cairosvg.svg2png(bytestring=self._starbridge_svg()))
        )

    @staticmethod
    def _starbridge_svg() -> str:
        """Image of starbridge, generated with Claude (Sonnet 3.5 new)"""
        return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
    <!-- Background -->
    <rect width="256" height="256" fill="#1a1a2e"/>
    
    <!-- Stars in background -->
    <circle cx="30" cy="40" r="1" fill="white"/>
    <circle cx="80" cy="30" r="1.5" fill="white"/>
    <circle cx="150" cy="45" r="1" fill="white"/>
    <circle cx="200" cy="25" r="1.5" fill="white"/>
    <circle cx="220" cy="60" r="1" fill="white"/>
    <circle cx="50" cy="70" r="1" fill="white"/>
    <circle cx="180" cy="80" r="1.5" fill="white"/>
    
    <!-- Bridge structure -->
    <!-- Left support -->
    <path d="M40 180 L60 100 L80 180" fill="#4a4e69"/>
    <!-- Right support -->
    <path d="M176 180 L196 100 L216 180" fill="#4a4e69"/>
    
    <!-- Bridge deck -->
    <path d="M30 180 L226 180" stroke="#9a8c98" stroke-width="8" fill="none"/>
    
    <!-- Suspension cables -->
    <path d="M60 100 C128 50, 128 50, 196 100" stroke="#c9ada7" stroke-width="3" fill="none"/>
    <path d="M60 100 L80 180" stroke="#c9ada7" stroke-width="2" fill="none"/>
    <path d="M196 100 L176 180" stroke="#c9ada7" stroke-width="2" fill="none"/>
    
    <!-- Star decorations -->
    <path d="M128 70 L132 62 L140 60 L132 58 L128 50 L124 58 L116 60 L124 62 Z" fill="#ffd700"/>
    <path d="M60 95 L62 91 L66 90 L62 89 L60 85 L58 89 L54 90 L58 91 Z" fill="#ffd700"/>
    <path d="M196 95 L198 91 L202 90 L198 89 L196 85 L194 89 L190 90 L194 91 Z" fill="#ffd700"/>
    
    <!-- Reflection in water -->
    <path d="M40 180 L60 220 L80 180 M176 180 L196 220 L216 180" fill="#1a1a2e" opacity="0.3"/>
    <path d="M60 100 C128 150, 128 150, 196 100" stroke="#c9ada7" stroke-width="1" fill="none" opacity="0.2"/>
</svg>"""
