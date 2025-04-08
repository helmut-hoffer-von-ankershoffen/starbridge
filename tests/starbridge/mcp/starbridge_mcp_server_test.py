"""Test the MCP server functionality."""

import asyncio
import base64
import os
import signal
import subprocess
import time
from pathlib import Path

import pytest
import requests
from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client
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

from starbridge.hello import Service as HelloService
from tests.utils_test import _server_parameters

try:
    from starbridge.hello.cli import bridge
except ImportError:
    bridge = None

MOCK_GET_ALL_SPACES = "atlassian.Confluence.get_all_spaces"
MOCK_GET_SPACE = "atlassian.Confluence.get_space"
PYPROJECT_TOML = "pyproject.toml"
DOT_COVERAGE = ".coverage"

EXPECTED_TOOLS = [
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
    "starbridge_hello_health",
    "starbridge_hello_hello",
    "starbridge_hello_info",
    "starbridge_hello_pdf",
]


@pytest.fixture
def runner() -> CliRunner:
    """Get a Click CLI test runner."""
    return CliRunner()


@pytest.mark.asyncio
async def test_mcp_server_list_tools_stdio() -> None:
    """Test listing of tools from the server."""
    # Expected tool names that should be present
    expected_tools = EXPECTED_TOOLS.copy()
    if bridge:
        expected_tools.append("starbridge_hello_bridge")

    async with stdio_client(_server_parameters()) as (read, write), ClientSession(read, write) as session:
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
async def test_mcp_server_list_tools_sse() -> None:
    """Test listing of tools from the server in sse mode."""
    expected_tools = EXPECTED_TOOLS.copy()

    # Start the server in SSE mode
    env = os.environ.copy()
    env.update({
        "COVERAGE_PROCESS_START": PYPROJECT_TOML,
        "COVERAGE_FILE": os.getenv("COVERAGE_FILE", DOT_COVERAGE),
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
        async with (
            sse_client(
                "http://0.0.0.0:8002/sse",
                timeout=1,
                sse_read_timeout=1,
            ) as (read, write),
            ClientSession(read, write) as session,
        ):
            await session.initialize()

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
async def test_mcp_server_list_resources() -> None:
    """Test listing of resources from the server."""
    async with (
        stdio_client(_server_parameters([MOCK_GET_ALL_SPACES])) as (read, write),
        ClientSession(read, write) as session,
    ):
        await session.initialize()

        result = await session.list_resources()

        assert result.resources is not None
        assert len(result.resources) == 1
        assert any(
            resource.name == "helmut"
            for resource in result.resources
            if str(resource.uri) == "starbridge://confluence/space/~7120201709026d2b41448e93bb58d5fa301026"
        )


@pytest.mark.asyncio
async def test_mcp_server_read_resource() -> None:
    """Test reading a resource from the server."""
    async with (
        stdio_client(
            _server_parameters([
                MOCK_GET_ALL_SPACES,
                MOCK_GET_SPACE,
            ]),
        ) as (
            read,
            write,
        ),
        ClientSession(read, write) as session,
    ):
        await session.initialize()

        result = await session.read_resource(
            AnyUrl(
                "starbridge://confluence/space/~7120201709026d2b41448e93bb58d5fa301026",
            ),
        )
        assert len(result.contents) == 1
        content = result.contents[0]
        assert type(content) is TextResourceContents
        assert content.text == Path("tests/fixtures/get_space.json").read_text(encoding="utf-8")


@pytest.mark.asyncio
async def test_mcp_server_list_prompts() -> None:
    """Test listing of prompts from the server."""
    async with stdio_client(_server_parameters()) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        result = await session.list_prompts()

        assert result.prompts is not None


@pytest.mark.asyncio
async def test_mcp_server_prompt_get() -> None:
    """Test getting a prompt from the server."""
    async with (
        stdio_client(_server_parameters([MOCK_GET_ALL_SPACES])) as (read, write),
        ClientSession(read, write) as session,
    ):
        await session.initialize()

        result = await session.get_prompt(
            "starbridge_confluence_space_summary",
            {"style": "detailed"},
        )

        assert len(result.messages) == 1
        message = result.messages[0]
        assert type(message) is PromptMessage
        assert type(message.content) is TextContent
        assert (
            message.content.text == "Here are the current spaces to summarize: Give extensive details.\n\n"
            "- ~7120201709026d2b41448e93bb58d5fa301026: helmut (personal)"
        )


@pytest.mark.asyncio
async def test_mcp_server_tool_call() -> None:
    """Test calling a tool on the server."""
    async with stdio_client(_server_parameters()) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        result = await session.call_tool("starbridge_hello_hello", {})
        assert len(result.content) == 1
        content = result.content[0]
        assert type(content) is TextContent
        assert content.text == "Hello World!"

        result = await session.call_tool(
            "starbridge_hello_hello",
            {"locale": "de_DE"},
        )
        assert len(result.content) == 1
        content = result.content[0]
        assert type(content) is TextContent
        assert content.text == "Hallo Welt!"


if hasattr(HelloService, "bridge"):  # if extra imaging

    @pytest.mark.asyncio
    async def test_mcp_server_tool_call_with_image() -> None:
        """Test calling a tool with image content on the server."""
        async with stdio_client(_server_parameters()) as (read, write), ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool("starbridge_hello_bridge", {})
            assert len(result.content) == 1
            content = result.content[0]
            assert type(content) is ImageContent
            assert content.data == base64.b64encode(
                Path("tests/fixtures/starbridge.png").read_bytes(),
            ).decode("utf-8")


@pytest.mark.asyncio
async def test_mcp_server_tool_call_with_pdf() -> None:
    """Test calling a tool with PDF content on the server."""
    async with stdio_client(_server_parameters()) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        result = await session.call_tool("starbridge_hello_pdf", {})
        assert len(result.content) == 1
        content = result.content[0]
        assert type(content) is EmbeddedResource
        assert type(content.resource) is BlobResourceContents
        assert content.resource.mimeType == "application/pdf"
        assert content.resource.blob == base64.b64encode(
            Path("tests/fixtures/starbridge.pdf").read_bytes(),
        ).decode("utf-8")


@pytest.mark.skip(reason="test_core_env_args_passed disabled temporarily")
def test_mcp_server_sse_terminates(runner) -> None:
    """Test if SSE server terminates correctly."""
    env = os.environ.copy()
    env.update({
        "COVERAGE_PROCESS_START": PYPROJECT_TOML,
        "COVERAGE_FILE": os.getenv("COVERAGE_FILE", DOT_COVERAGE),
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
        time.sleep(10)

        # Send terminate request
        try:
            response = requests.get("http://0.0.0.0:9000/terminate", timeout=10)
            response.raise_for_status()
        except Exception:  # noqa: S110, BLE001
            pass

        # Wait for process to end (timeout after 5 seconds)
        process.wait(timeout=10)

        assert process.returncode == 0

    finally:
        process.terminate()
        process.kill()
