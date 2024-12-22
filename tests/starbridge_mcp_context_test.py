import pytest

from starbridge.mcp import MCPContext, MCPServer


async def test_read_request_fails_outside_server():
    """Test listing of tools from the server"""
    server = MCPServer()
    context = MCPContext(server=server, request_context=None)
    # Assert that calling context.request_context() raises a RuntimeError
    with pytest.raises(RuntimeError):
        context.request_context  # noqa: B018
