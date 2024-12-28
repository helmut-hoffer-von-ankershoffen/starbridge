import json
import os
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from starbridge.cli import cli

MOCK_GET_ALL_SPACES = "atlassian.Confluence.get_all_spaces"
MOCK_GET_SPACE = "atlassian.Confluence.get_space"
PYPROJECT_TOML = "pyproject.toml"
DOT_COVERAGE = ".coverage"


@pytest.fixture
def runner():
    return CliRunner()


def test_mcp_services(runner):
    """Check available services."""
    result = runner.invoke(cli, ["mcp", "services"])
    assert result.exit_code == 0

    # We expect these three services to be present
    expected_services = [
        "starbridge.claude.service.Service",
        "starbridge.confluence.service.Service",
        "starbridge.hello.service.Service",
    ]

    for service in expected_services:
        assert service in result.stdout


def test_mcp_tools(runner):
    """Check available tools."""
    result = runner.invoke(cli, ["mcp", "tools"])
    assert result.exit_code == 0

    # All expected tool names
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

    output = result.stdout
    for tool in expected_tools:
        assert f"name='{tool}'" in output


def test_mcp_tool(runner):
    """Check a tool."""
    result = runner.invoke(
        cli, ["mcp", "tool", "starbridge_hello_hello", "--arguments", "locale=de_DE"]
    )
    assert result.exit_code == 0
    assert "Hallo Welt!" in result.stdout


def test_mcp_prompts(runner):
    """Check available tools."""
    result = runner.invoke(cli, ["mcp", "prompts"])
    assert result.exit_code == 0
    assert "starbridge_confluence_space_summary" in result.stdout


@patch(MOCK_GET_ALL_SPACES)
def test_mcp_prompt(mock_get_all_spaces, runner):
    """Check available resources."""
    # Mock the response data that would come from get_all_spaces
    with Path("tests/fixtures/get_all_spaces.json").open() as f:
        mock_get_all_spaces.return_value = json.loads(f.read())

    result = runner.invoke(
        cli,
        [
            "mcp",
            "prompt",
            "starbridge_confluence_space_summary",
            "--arguments",
            "style=detailed",
        ],
    )

    assert result.exit_code == 0
    assert "details" in result.stdout


def test_mcp_resource_types(runner):
    """Check available resources."""
    result = runner.invoke(cli, ["mcp", "resource-types"])
    assert result.exit_code == 0
    assert "starbridge://confluence/space" in result.stdout


@patch(MOCK_GET_ALL_SPACES)
def test_mcp_resources(mock_get_all_spaces, runner):
    """Check available resources."""
    # Mock the response data that would come from get_all_spaces
    with Path("tests/fixtures/get_all_spaces.json").open() as f:
        mock_get_all_spaces.return_value = json.loads(f.read())

    result = runner.invoke(cli, ["mcp", "resources"])
    assert result.exit_code == 0
    assert "7120201709026d2b41448e93bb58d" in result.stdout  # pragma: allowlist secret


@patch(MOCK_GET_SPACE)
def test_mcp_resource(mock_get_space, runner):
    """Read a resource."""
    # Mock the response data that would come from get_all_spaces
    with Path("tests/fixtures/get_space.json").open() as f:
        mock_get_space.return_value = json.loads(f.read())

    result = runner.invoke(
        cli,
        [
            "mcp",
            "resource",
            "starbridge://confluence/space/~7120201709026d2b41448e93bb58d5fa301026",  # pragma: allowlist secret
        ],
    )
    assert result.exit_code == 0
    assert "7120201709026d2b41448e93bb58d" in result.stdout  # pragma: allowlist secret


def test_mcp_inspector(runner):
    env = os.environ.copy()
    env.update({
        "COVERAGE_PROCESS_START": PYPROJECT_TOML,
        "COVERAGE_FILE": os.getenv("COVERAGE_FILE", DOT_COVERAGE),
        "MOCKS": "webbrowser.open",
        "MOCK_WEBBROWSER_OPEN": "return_value=None",
        "CLIENT_PORT": "5174",
        "SERVER_PORT": "3001",
    })

    process = None
    try:
        process = subprocess.run(
            ["uv", "run", "starbridge", "mcp", "inspect"],
            capture_output=True,
            timeout=10,
            text=True,
            env=env,
        )
    except subprocess.TimeoutExpired as e:
        process = e.stdout

    # Handle both cases where process completed or timed out
    if isinstance(process, subprocess.CompletedProcess):
        assert "Opened browser pointing to MCP Inspector" in process.stdout
    else:
        assert process is not None, "Process failed to execute"
