import asyncio
import base64
import os
import signal
import subprocess
import time
from pathlib import Path

import pytest
import requests
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import get_default_environment, stdio_client
from mcp.types import (
    BlobResourceContents,
    EmbeddedResource,
    ImageContent,
    PromptMessage,
    TextContent,
    TextResourceContents,
)
from pydantic import AnyUrl
from typer.testing import CliRunner


@pytest.fixture
def runner():
    return CliRunner()


def _server_parameters(mocks: list[str] | None = None) -> StdioServerParameters:
    """Create server parameters with coverage enabled"""
    env = dict(get_default_environment())
    # Add coverage config to subprocess
    env.update({
        "COVERAGE_PROCESS_START": "pyproject.toml",
        "COVERAGE_FILE": os.getenv("COVERAGE_FILE", ".coverage"),
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


@pytest.mark.skip(reason="SSE test disabled temporarily")
@pytest.mark.asyncio
async def test_mcp_server_list_tools_sse():
    """Test listing of tools from the server in sse mode"""
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

    # Start the server in SSE mode
    env = os.environ.copy()
    env.update({
        "COVERAGE_PROCESS_START": "pyproject.toml",
        "COVERAGE_FILE": os.getenv("COVERAGE_FILE", ".coverage"),
        "PYTHONPATH": ".",
    })

    process = await asyncio.create_subprocess_exec(
        "uv",
        "run",
        "starbridge",
        "mcp",
        "serve",
        "--host",
        "0.0.0.0",
        "--port",
        "8002",
        env=env,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    try:
        # Give the server a moment to start up
        await asyncio.sleep(2)

        # Connect to the server using SSE
        async with sse_client(
            "http://0.0.0.0:8002/sse", timeout=1, sse_read_timeout=1
        ) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()

                # List available tools
                result = await session.list_tools()

                # Verify each expected tool is present
                tool_names = [tool.name for tool in result.tools]
                for expected_tool in expected_tools:
                    assert expected_tool in tool_names

        process.terminate()

    finally:
        process.terminate()
        # Clean up the subprocess
        if process.returncode is None:
            process.send_signal(signal.SIGTERM)
            await process.wait()


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
async def test_mcp_server_read_resource():
    """Test getting prompt from server"""
    async with stdio_client(
        _server_parameters([
            "atlassian.Confluence.get_all_spaces",
            "atlassian.Confluence.get_space",
        ])
    ) as (
        read,
        write,
    ):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # List available prompts
            result = await session.read_resource(
                AnyUrl(
                    "starbridge://confluence/space/~7120201709026d2b41448e93bb58d5fa301026"
                )
            )
            assert len(result.contents) == 1
            content = result.contents[0]
            assert type(content) is TextResourceContents
            assert content.text == Path("tests/fixtures/get_space.json").read_text()


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
async def test_mcp_server_prompt_get():
    """Test getting prompt from server"""
    async with stdio_client(
        _server_parameters(["atlassian.Confluence.get_all_spaces"])
    ) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # List available prompts
            result = await session.get_prompt(
                "starbridge_confluence_space_summary", {"style": "detailed"}
            )

            assert len(result.messages) == 1
            message = result.messages[0]
            assert type(message) is PromptMessage
            assert type(message.content) is TextContent
            assert (
                message.content.text
                == "Here are the current spaces to summarize: Give extensive details.\n\n- ~7120201709026d2b41448e93bb58d5fa301026: helmut (personal)"
            )


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

            # List available prompts
            result = await session.call_tool(
                "starbridge_hello_hello", {"locale": "de_DE"}
            )
            assert len(result.content) == 1
            content = result.content[0]
            assert type(content) is TextContent
            assert content.text == "Hallo Welt!"


@pytest.mark.asyncio
async def test_mcp_server_tool_call_with_image():
    """Test listing of prompts from the server"""
    async with stdio_client(_server_parameters()) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # List available prompts
            result = await session.call_tool("starbridge_hello_bridge", {})
            assert len(result.content) == 1
            content = result.content[0]
            assert type(content) is ImageContent
            assert content.data == base64.b64encode(
                Path("tests/fixtures/starbridge.png").read_bytes()
            ).decode("utf-8")


@pytest.mark.asyncio
async def test_mcp_server_tool_call_with_pdf():
    """Test listing of prompts from the server"""
    async with stdio_client(_server_parameters()) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # List available prompts
            result = await session.call_tool("starbridge_hello_pdf", {})
            assert len(result.content) == 1
            content = result.content[0]
            assert type(content) is EmbeddedResource
            assert type(content.resource) is BlobResourceContents
            assert content.resource.mimeType == "application/pdf"
            assert content.resource.blob == base64.b64encode(
                Path("tests/fixtures/starbridge.pdf").read_bytes()
            ).decode("utf-8")


def test_mcp_server_sse_terminates(runner):
    env = os.environ.copy()
    env.update({
        "COVERAGE_PROCESS_START": "pyproject.toml",
        "COVERAGE_FILE": os.getenv("COVERAGE_FILE", ".coverage"),
        "MOCKS": "webbrowser.open",
    })

    process = subprocess.Popen(
        [
            "uv",
            "run",
            "starbridge",
            "mcp",
            "serve",
            "--host",
            "0.0.0.0",
            "--port",
            "9000",
        ],
        text=True,
        env=env,
    )

    try:
        # Give the server time to start
        time.sleep(5)

        # Send terminate request
        try:
            response = requests.get("http://0.0.0.0:9000/terminate")
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            pass

        # Wait for process to end (timeout after 5 seconds)
        process.wait(timeout=5)

        assert process.returncode == 1

    finally:
        # Ensure process is terminated even if test fails
        if process.poll() is None:
            process.kill()
