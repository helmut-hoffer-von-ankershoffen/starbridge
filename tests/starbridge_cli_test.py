import pytest
from typer.testing import CliRunner

from starbridge.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_built_with_love(runner):
    """Check epilog shown."""
    result = runner.invoke(
        cli,
        ["--help"],
        terminal_width=80,
    )
    assert result.exit_code == 0
    assert "built with love in Berlin" in result.output


def test_invalid_command(runner):
    """Test invalid command returns error"""
    result = runner.invoke(cli, ["invalid"])
    assert result.exit_code != 0
