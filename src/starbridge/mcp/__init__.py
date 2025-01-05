"""MCP implementation for starbridge."""

from .cli import cli, serve
from .context import MCPContext
from .decorators import mcp_prompt, mcp_resource, mcp_resource_iterator, mcp_tool
from .models import PromptMetadata, ResourceMetadata
from .server import MCPServer
from .service import MCPBaseService

__all__ = [
    "MCPBaseService",
    "MCPContext",
    "MCPServer",
    "PromptMetadata",
    "ResourceMetadata",
    "cli",
    "mcp_prompt",
    "mcp_resource",
    "mcp_resource_iterator",
    "mcp_tool",
    "serve",
]
