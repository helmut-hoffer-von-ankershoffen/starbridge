import pytest
from typer.testing import CliRunner

from starbridge.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_mcp_tools(runner):
    """Check tools include listing spaces and creating pages."""
    result = runner.invoke(cli, ["confluence", "mcp", "tools"])
    assert result.exit_code == 0
    assert "name='starbridge_confluence_info'" in result.stdout
    assert "name='starbridge_confluence_page_create'" in result.stdout
    assert "name='starbridge_confluence_space_list'" in result.stdout
