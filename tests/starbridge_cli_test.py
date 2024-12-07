import pytest
from typer.testing import CliRunner

from starbridge.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_built_with_love(runner):
    """Check epilog shown."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert (
        "Built with love in Berlin by Helmut Hoffer von Ankershoffen" in result.stdout
    )


def test_invalid_command(runner):
    """Test invalid command returns error"""
    result = runner.invoke(cli, ["invalid"])
    assert result.exit_code != 0
