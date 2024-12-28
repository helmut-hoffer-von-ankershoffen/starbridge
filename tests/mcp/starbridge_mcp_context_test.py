import pytest

from starbridge.instrumentation import logfire_initialize
from starbridge.mcp import MCPContext, MCPServer

logfire_initialize()


def test_read_request_fails_outside_server():
    """Test listing of tools from the server"""
    server = MCPServer()
    context = MCPContext(server=server, request_context=None)
    # Assert that calling context.request_context() raises a RuntimeError
    with pytest.raises(RuntimeError):
        context.request_context  # noqa: B018
