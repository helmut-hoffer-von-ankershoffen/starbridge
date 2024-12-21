import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def _server_parameters():
    return StdioServerParameters(
        command="uv",
        args=["run", "--no-dev", "starbridge"],
        env=None,
    )


@pytest.mark.asyncio
async def test_mcp_client_tools():
    """Test listing of MCP tools via client connection"""

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
