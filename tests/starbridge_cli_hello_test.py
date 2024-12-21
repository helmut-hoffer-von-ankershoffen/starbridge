from pathlib import Path

import pytest
from typer.testing import CliRunner

from starbridge.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_hello_bridge(runner):
    """Check we dump the image."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["hello", "bridge", "--dump"])
        assert result.exit_code == 0
        assert Path("starbridge.png").is_file()
        assert Path("starbridge.png").stat().st_size == 6235


def test_hello_pdf(runner):
    """Check we dump the image."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["hello", "pdf", "--dump"])
        assert result.exit_code == 0
        assert Path("starbridge.pdf").is_file()
        assert Path("starbridge.pdf").stat().st_size == 6840
