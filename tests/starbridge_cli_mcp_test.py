import json
import os
import subprocess
import time
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from starbridge.cli import cli


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
    result = runner.invoke(cli, ["mcp", "tool", "starbridge_hello_hello"])
    assert result.exit_code == 0
    assert "Hello World!" in result.stdout


def test_mcp_prompts(runner):
    """Check available tools."""
    result = runner.invoke(cli, ["mcp", "prompts"])
    assert result.exit_code == 0
    assert "starbridge_confluence_space_summary" in result.stdout


@patch("atlassian.Confluence.get_all_spaces")
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


@patch("atlassian.Confluence.get_all_spaces")
def test_mcp_resources(mock_get_all_spaces, runner):
    """Check available resources."""
    # Mock the response data that would come from get_all_spaces
    with Path("tests/fixtures/get_all_spaces.json").open() as f:
        mock_get_all_spaces.return_value = json.loads(f.read())

    result = runner.invoke(cli, ["mcp", "resources"])
    assert result.exit_code == 0
    assert "7120201709026d2b41448e93bb58d" in result.stdout


@patch("atlassian.Confluence.get_space")
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
            "starbridge://confluence/space/~7120201709026d2b41448e93bb58d5fa301026",
        ],
    )
    assert result.exit_code == 0
    assert "7120201709026d2b41448e93bb58d" in result.stdout


def test_mcp_inspector(runner):
    expected_msg = "MCP Inspector is up and running"
    env = os.environ.copy()
    env.update({
        "COVERAGE_PROCESS_START": "pyproject.toml",
        "COVERAGE_FILE": os.getenv("COVERAGE_FILE", ".coverage"),
        "PYTHONPATH": ".",
        "MOCKS": "webbrowser.open",
    })

    process = subprocess.Popen(
        ["uv", "run", "starbridge", "mcp", "inspect"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )

    found_expected_msg = False
    output_lines = []
    out = ""
    err = ""

    try:
        start_time = time.time()
        while time.time() - start_time < 10:
            if process.stdout is None:
                break

            line = process.stdout.readline()
            if line:
                output_lines.append(line)
            if expected_msg in line:
                found_expected_msg = True
                break

            if process.poll() is not None:
                break

            time.sleep(0.1)

        # Get any remaining output
        try:
            out, err = process.communicate(timeout=1)
            out = "\n".join(output_lines) + (out or "")
            if not found_expected_msg:
                found_expected_msg = expected_msg in out
        except subprocess.TimeoutExpired:
            out = "\n".join(output_lines)
            err = ""

        assert found_expected_msg, (
            f"Expected message '{expected_msg}' not found in output. STDOUT: {out}, STDERR: {err}"
        )
    finally:
        process.kill()
