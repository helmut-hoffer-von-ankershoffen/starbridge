from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from typer.testing import CliRunner

from starbridge.cli import cli

SUBPROCESS_RUN = "subprocess.run"


@pytest.fixture
def runner():
    return CliRunner()


@patch("platform.system", return_value="Darwin")
@patch("psutil.process_iter")
@patch("starbridge.claude.service.Service.is_installed", return_value=True)
def test_claude_cli_health(mock_has_config, mock_process_iter, mock_platform, runner):
    """Check health"""
    mock_process = Mock()
    mock_process.info = {"name": "Claude"}
    mock_process_iter.return_value = [mock_process]

    result = runner.invoke(cli, ["claude", "health"])
    assert '"UP"' in result.stdout
    assert result.exit_code == 0


def test_claude_cli_info(runner):
    """Check info spots running process uv"""
    result = runner.invoke(cli, ["claude", "info"])
    assert result.exit_code == 0
    assert "pid" in result.stdout


def test_claude_cli_log(runner: CliRunner, tmp_path: Path) -> None:
    """Check log command."""
    log_path = tmp_path / "claude.log"
    log_path.write_text(data="Logging")

    with (
        patch(
            "starbridge.claude.service.Service.log_path",
            return_value=tmp_path / "claude.log",
        ),
        patch(SUBPROCESS_RUN) as mock_run,
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
