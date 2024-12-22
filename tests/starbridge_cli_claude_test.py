from pathlib import Path
from unittest.mock import patch

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


def test_claude_log(runner: CliRunner, tmp_path: Path) -> None:
    """Check log command."""
    log_path = tmp_path / "claude.log"
    log_path.write_text(data="Logging")

    with (
        patch(
            "starbridge.claude.service.Service.log_path",
            return_value=tmp_path / "claude.log",
        ),
        patch("subprocess.run") as mock_run,
    ):
        result = runner.invoke(cli, ["claude", "log"])
        assert result.exit_code == 0
        mock_run.assert_called_once()
        assert mock_run.call_args[0][0] == [
            "tail",
            "-n",
            "100",
            str(log_path),
        ]
