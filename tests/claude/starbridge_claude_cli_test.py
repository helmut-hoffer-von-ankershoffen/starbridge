from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from typer.testing import CliRunner

from starbridge.claude.service import Service
from starbridge.cli import cli

SUBPROCESS_RUN = "subprocess.run"


@pytest.fixture
def runner():
    return CliRunner()


@patch("platform.system", return_value="Darwin")
@patch("psutil.process_iter")
@patch("starbridge.claude.service.Service.is_installed", return_value=True)
def test_claude_health(mock_has_config, mock_process_iter, mock_platform, runner):
    """Check health"""
    mock_process = Mock()
    mock_process.info = {"name": "Claude"}
    mock_process_iter.return_value = [mock_process]

    result = runner.invoke(cli, ["claude", "health"])
    assert '"UP"' in result.stdout
    assert result.exit_code == 0


def test_claude_info(runner):
    """Check info spots running process uv"""
    result = runner.invoke(cli, ["claude", "info"])
    assert result.exit_code == 0
    assert "pid" in result.stdout


def test_claude_log(runner: CliRunner, tmp_path: Path) -> None:
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


class TestClaudeService:
    @pytest.fixture
    def mock_darwin(self):
        with patch("platform.system", return_value="Darwin"):
            yield

    def test_claude_install_via_brew_already_installed(self, mock_darwin):
        with patch(SUBPROCESS_RUN) as mock_run:
            mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

            result = Service.install_via_brew()
            assert result is False

            mock_run.assert_called_once_with(
                ["brew", "list", "--cask", "claude"],
                capture_output=True,
                text=True,
                check=False,
            )

    def test_claude_install_via_brew_success(self, mock_darwin):
        with patch(SUBPROCESS_RUN) as mock_run:
            # First call returns 1 (not installed), second call returns 0 (install success)
            mock_run.side_effect = [
                Mock(returncode=1, stdout="", stderr=""),
                Mock(returncode=0, stdout="", stderr=""),
            ]

            result = Service.install_via_brew()
            assert result is True

            assert mock_run.call_count == 2
            mock_run.assert_any_call(
                ["brew", "list", "--cask", "claude"],
                capture_output=True,
                text=True,
                check=False,
            )
            mock_run.assert_any_call(
                ["brew", "install", "--cask", "claude"],
                capture_output=True,
                text=True,
                check=False,
            )

    def test_claude_install_via_brew_error(self, mock_darwin):
        with patch(SUBPROCESS_RUN) as mock_run:
            mock_run.side_effect = [
                Mock(returncode=1, stdout="", stderr=""),
                Mock(returncode=1, stdout="", stderr="Installation failed"),
            ]

            with pytest.raises(
                RuntimeError, match="Failed to install Claude: Installation failed"
            ):
                Service.install_via_brew()

    def test_claude_uninstall_via_brew_not_installed(self, mock_darwin):
        with patch(SUBPROCESS_RUN) as mock_run:
            mock_run.return_value = Mock(returncode=1, stdout="", stderr="")

            result = Service.uninstall_via_brew()
            assert result is False

            mock_run.assert_called_once_with(
                ["brew", "list", "--cask", "claude"],
                capture_output=True,
                text=True,
                check=False,
            )

    def test_claude_uninstall_via_brew_success(self, mock_darwin):
        with patch(SUBPROCESS_RUN) as mock_run:
            # First call returns 0 (installed), second call returns 0 (uninstall success)
            mock_run.side_effect = [
                Mock(returncode=0, stdout="", stderr=""),
                Mock(returncode=0, stdout="", stderr=""),
            ]

            result = Service.uninstall_via_brew()
            assert result is True

            assert mock_run.call_count == 2
            mock_run.assert_any_call(
                ["brew", "list", "--cask", "claude"],
                capture_output=True,
                text=True,
                check=False,
            )
            mock_run.assert_any_call(
                ["brew", "uninstall", "--cask", "claude"],
                capture_output=True,
                text=True,
                check=False,
            )

    def test_claude_uninstall_via_brew_error(self, mock_darwin):
        with patch(SUBPROCESS_RUN) as mock_run:
            mock_run.side_effect = [
                Mock(returncode=0, stdout="", stderr=""),
                Mock(returncode=1, stdout="", stderr="Uninstallation failed"),
            ]

            with pytest.raises(
                RuntimeError, match="Failed to uninstall Claude: Uninstallation failed"
            ):
                Service.uninstall_via_brew()
