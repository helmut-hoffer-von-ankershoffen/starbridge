"""Claude Desktop application integration module."""

from .cli import cli
from .service import Service
from .util import generate_mcp_server_config

__all__ = ["Service", "cli", "generate_mcp_server_config"]
