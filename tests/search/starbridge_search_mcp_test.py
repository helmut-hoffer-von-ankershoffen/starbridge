import pytest
from mcp import ClientSession
from mcp.client.stdio import stdio_client
from mcp.types import TextContent
from typer.testing import CliRunner

from ..utils_test import _server_parameters

PYPROJECT_TOML = "pyproject.toml"
DOT_COVERAGE = ".coverage"


@pytest.fixture
def runner():
    return CliRunner()


@pytest.mark.asyncio
async def test_search_mcp_tool_web():
    """Test server tool search"""
    async with stdio_client(_server_parameters()) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "starbridge_search_web",
                {"q": "hello world"},
            )
            assert len(result.content) == 1
            content = result.content[0]
            assert type(content) is TextContent
            assert "hello" in content.text
