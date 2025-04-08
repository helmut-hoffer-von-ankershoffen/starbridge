"""Tests for MCP context functionality."""

import pytest

from starbridge.instrumentation import logfire_initialize
from starbridge.mcp import MCPContext

logfire_initialize()


def test_mcp_context_read_request_fails_outside_server() -> None:
    """Test listing of tools from the server."""
    context = MCPContext(request_context=None)
    # Assert that calling context.request_context() raises a RuntimeError
    with pytest.raises(RuntimeError):
        context.request_context  # noqa: B018
