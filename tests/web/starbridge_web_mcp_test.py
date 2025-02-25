"""Test web MCP functionality."""

import pytest
from mcp import ClientSession
from mcp.client.stdio import stdio_client
from mcp.types import (
    TextContent,
)
from typer.testing import CliRunner

from tests.utils_test import _server_parameters

GET_TEST_URL = "https://starbridge.readthedocs.io/en/latest/"

PYPROJECT_TOML = "pyproject.toml"
DOT_COVERAGE = ".coverage"


@pytest.fixture
def runner() -> CliRunner:
    """Get a Click CLI test runner."""
    return CliRunner()


@pytest.mark.asyncio
async def test_web_mcp_tool_get() -> None:
    """Test server tool get."""
    async with stdio_client(_server_parameters()) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        result = await session.call_tool(
            "starbridge_web_get",
            {
                "url": GET_TEST_URL,
                "transform_to_markdown": True,
                "extract_links": False,
                "additional_context": False,
            },
        )
        assert len(result.content) == 1
        content = result.content[0]
        assert type(content) is TextContent
        assert "starbridge" in content.text
