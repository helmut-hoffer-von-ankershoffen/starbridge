import pytest
from typer.testing import CliRunner

from starbridge.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_claude_info(runner):
    """Check info spots running process uv"""
    result = runner.invoke(cli, ["claude", "info"])
    assert result.exit_code == 0
    assert "uv" in result.stdout
