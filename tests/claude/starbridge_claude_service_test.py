from unittest.mock import Mock, patch

import pytest

from starbridge.claude.service import Service

SUBPROCESS_RUN = "subprocess.run"


class TestClaudeService:
    @pytest.fixture
    def mock_darwin(self):
        with patch("platform.system", return_value="Darwin"):
            yield

    def test_claude_service_install_via_brew_already_installed(self, mock_darwin):
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

    def test_claude_service_install_via_brew_success(self, mock_darwin):
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

    def test_claude_service_install_via_brew_error(self, mock_darwin):
        with patch(SUBPROCESS_RUN) as mock_run:
            mock_run.side_effect = [
                Mock(returncode=1, stdout="", stderr=""),
                Mock(returncode=1, stdout="", stderr="Installation failed"),
            ]

            with pytest.raises(
                RuntimeError, match="Failed to install Claude: Installation failed"
            ):
                Service.install_via_brew()

    def test_claude_service_uninstall_via_brew_not_installed(self, mock_darwin):
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

    def test_claude_service_uninstall_via_brew_success(self, mock_darwin):
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

    def test_claude_service_uninstall_via_brew_error(self, mock_darwin):
        with patch(SUBPROCESS_RUN) as mock_run:
            mock_run.side_effect = [
                Mock(returncode=0, stdout="", stderr=""),
                Mock(returncode=1, stdout="", stderr="Uninstallation failed"),
            ]

            with pytest.raises(
                RuntimeError, match="Failed to uninstall Claude: Uninstallation failed"
            ):
                Service.uninstall_via_brew()
