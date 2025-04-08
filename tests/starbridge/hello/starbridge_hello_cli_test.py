"""Tests for Hello World CLI functionality."""

from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from starbridge.cli import cli

try:
    from starbridge.hello.cli import bridge
except ImportError:
    bridge = None


@pytest.fixture
def runner() -> CliRunner:
    """Get a Click CLI test runner."""
    return CliRunner()


def test_hello_cli_info(runner) -> None:
    """Check hello info."""
    result = runner.invoke(cli, ["hello", "info"])
    assert "en_US" in result.output
    assert result.exit_code == 0


def test_hello_cli_health(runner) -> None:
    """Check hello health."""
    result = runner.invoke(cli, ["hello", "health"])
    assert '"UP"' in result.output
    assert result.exit_code == 0


if bridge:  # if extra imaging

    def test_hello_cli_bridge(runner) -> None:
        """Check we dump the image."""
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ["hello", "bridge", "--dump"])
            assert result.exit_code == 0
            assert Path("starbridge.png").is_file()
            assert Path("starbridge.png").stat().st_size == 6235

    @patch("cairosvg.svg2png", side_effect=OSError)
    def test_hello_cli_bridge_error(mock_svg2png, runner) -> None:
        """Check we handle cairo missing."""
        result = runner.invoke(cli, ["hello", "bridge"])
        assert result.exit_code == 78

else:

    @pytest.mark.no_extras
    def test_hello_cli_no_imaging_extra_no_bridge(runner) -> None:
        """Check we handle missing PIL."""
        result = runner.invoke(cli, ["hello"])
        assert "Show image" not in result.output
        assert result.exit_code == 0


def test_hello_cli_pdf(runner) -> None:
    """Check we dump the pdf."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["hello", "pdf", "--dump"])
        assert result.exit_code == 0
        assert Path("starbridge.pdf").is_file()
        assert Path("starbridge.pdf").stat().st_size == 6840


@patch("sys.platform", new="linux")
@patch("subprocess.run")
def test_hello_cli_pdf_open(mock_run, runner) -> None:
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
