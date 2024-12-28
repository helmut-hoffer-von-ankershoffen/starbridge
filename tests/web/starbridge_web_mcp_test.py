import os

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import get_default_environment, stdio_client
from mcp.types import (
    TextContent,
)
from typer.testing import CliRunner

try:
    from starbridge.hello.cli import bridge
except ImportError:
    bridge = None

GET_TEST_URL = "https://helmuthva.gitbook.io/starbridge"

PYPROJECT_TOML = "pyproject.toml"
DOT_COVERAGE = ".coverage"


@pytest.fixture
def runner():
    return CliRunner()


def _server_parameters(mocks: list[str] | None = None) -> StdioServerParameters:
    """Create server parameters with coverage enabled"""
    env = dict(get_default_environment())
    # Add coverage config to subprocess
    env.update({
        "COVERAGE_PROCESS_START": PYPROJECT_TOML,
        "COVERAGE_FILE": os.getenv("COVERAGE_FILE", DOT_COVERAGE),
    })
    if (mocks is not None) and mocks:
        env.update({"MOCKS": ",".join(mocks)})

    return StdioServerParameters(
        command="uv",
        args=["run", "starbridge"],
        env=env,
    )


@pytest.mark.asyncio
async def test_web_mcp_tool_get():
    """Test listing of prompts from the server"""
    async with stdio_client(_server_parameters()) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "starbridge_web_get", {"url": GET_TEST_URL, "format": "markdown"}
            )
            assert len(result.content) == 1
            content = result.content[0]
            assert type(content) is TextContent
            assert "Starbridge[![](https://helmuthva.gitbook.io" in content.text
