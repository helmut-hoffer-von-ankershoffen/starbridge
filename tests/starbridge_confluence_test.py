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
    assert "name='starbridge-confluence-info'" in result.stdout
    assert "name='starbridge-confluence-page-create'" in result.stdout
    assert "name='starbridge-confluence-space-list'" in result.stdout
