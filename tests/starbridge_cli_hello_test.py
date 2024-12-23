from pathlib import Path
from unittest.mock import patch

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
    """Check we dump the pdf."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["hello", "pdf", "--dump"])
        assert result.exit_code == 0
        assert Path("starbridge.pdf").is_file()
        assert Path("starbridge.pdf").stat().st_size == 6840


@patch("sys.platform", new="linux")
@patch("subprocess.run")
def test_hello_pdf_open(mock_run, runner):
    """Check we open the pdf."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["hello", "pdf"])
        assert result.exit_code == 0

        # Verify xdg-open was called
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        assert args[0][0] == "xdg-open"
        assert str(args[0][1]).endswith(".pdf")
        assert kwargs["check"] is True


@patch("cairosvg.svg2png", side_effect=OSError)
def test_hello_bridge_error(mock_svg2png, runner):
    """Check we handle cairo missing."""
    result = runner.invoke(cli, ["hello", "bridge"])
    assert result.exit_code == 78
