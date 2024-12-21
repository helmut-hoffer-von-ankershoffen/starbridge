import os

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import get_default_environment, stdio_client
from mcp.types import TextContent


def _server_parameters(mocks: list[str] | None = None) -> StdioServerParameters:
    """Create server parameters with coverage enabled"""
    env = dict(get_default_environment())
    # Add coverage config to subprocess
    env.update({
        "COVERAGE_PROCESS_START": "pyproject.toml",
        "COVERAGE_FILE": os.getenv("COVERAGE_FILE", ".coverage"),
        "PYTHONPATH": ".",
    })
    if (mocks is not None) and mocks:
        env.update({"MOCKS": ",".join(mocks)})

    return StdioServerParameters(
        command="uv",
        args=["run", "starbridge"],
        env=env,
    )


@pytest.mark.asyncio
async def test_mcp_server_list_tools():
    """Test listing of tools from the server"""

    # Expected tool names that should be present
    expected_tools = [
        "starbridge_claude_health",
        "starbridge_claude_info",
        "starbridge_claude_restart",
        "starbridge_confluence_health",
        "starbridge_confluence_info",
        "starbridge_confluence_page_create",
        "starbridge_confluence_page_delete",
        "starbridge_confluence_page_get",
        "starbridge_confluence_page_list",
        "starbridge_confluence_page_update",
        "starbridge_confluence_space_list",
        "starbridge_hello_bridge",
        "starbridge_hello_health",
        "starbridge_hello_hello",
        "starbridge_hello_info",
        "starbridge_hello_pdf",
    ]

    async with stdio_client(_server_parameters()) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            result = await session.list_tools()

            # Verify each expected tool is present
            tool_names = [tool.name for tool in result.tools]
            for expected_tool in expected_tools:
                assert expected_tool in tool_names


@pytest.mark.asyncio
async def test_mcp_server_list_resources():
    async with stdio_client(
        _server_parameters(["atlassian.Confluence.get_all_spaces"])
    ) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # List available resources
            result = await session.list_resources()

            assert result.resources is not None
            assert len(result.resources) == 1
            assert any(
                resource.name == "helmut"
                for resource in result.resources
                if str(resource.uri)
                == "starbridge://confluence/space/~7120201709026d2b41448e93bb58d5fa301026"
            )


@pytest.mark.asyncio
async def test_mcp_server_list_prompts():
    """Test listing of prompts from the server"""
    async with stdio_client(_server_parameters()) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # List available prompts
            result = await session.list_prompts()

            assert result.prompts is not None


@pytest.mark.asyncio
async def test_mcp_server_tool_call():
    """Test listing of prompts from the server"""
    async with stdio_client(_server_parameters()) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # List available prompts
            result = await session.call_tool("starbridge_hello_hello", {})
            assert len(result.content) == 1
            content = result.content[0]
            assert type(content) is TextContent
            assert content.text == "Hello World!"
