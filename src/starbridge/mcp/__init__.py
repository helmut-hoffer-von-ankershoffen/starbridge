from .cli import cli  # Make CLI entrypoint available at package level
from .server import MCPServer

# Optionally expose other important items at package level
__all__ = ["cli", "MCPServer"]
