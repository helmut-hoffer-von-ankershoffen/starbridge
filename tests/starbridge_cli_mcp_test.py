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
