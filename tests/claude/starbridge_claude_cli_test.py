"""Tests for the Claude CLI functionality."""

import json
import os
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from typer.testing import CliRunner

from starbridge.cli import cli

SUBPROCESS_RUN = "subprocess.run"


@pytest.fixture
def runner() -> CliRunner:
    """Get a Click CLI test runner."""
    return CliRunner()


@patch("platform.system", return_value="Darwin")
@patch("psutil.process_iter")
@patch("starbridge.claude.service.Service.is_installed", return_value=True)
def test_claude_cli_health(mock_has_config, mock_process_iter, mock_platform, runner) -> None:
    """Check health spots Claude up and running."""
    mock_process = Mock()
    mock_process.info = {"pid": 1234, "name": "Claude"}
    mock_process_iter.return_value = [mock_process]

    result = runner.invoke(cli, ["claude", "health"])
    assert '"UP"' in result.stdout
    assert result.exit_code == 0


def test_claude_cli_health_in_container() -> None:
    """Check health spots Claude not running in container."""
    env = os.environ.copy()
    env.update({
        "COVERAGE_PROCESS_START": "pyproject.toml",
        "COVERAGE_FILE": os.getenv("COVERAGE_FILE", ".coverage"),
        "STARBRIDGE_RUNNING_IN_CONTAINER": "1",  # indicate we are running within a container
    })
    result = subprocess.run(
        ["uv", "run", "starbridge", "claude", "health"],
        capture_output=True,
        text=True,  # Get string output instead of bytes
        env=env,
        check=False,
    )
    assert result.returncode == 0
    assert '"DOWN"' in result.stdout


@patch("platform.system", return_value="Darwin")
@patch("psutil.process_iter")
@patch("starbridge.claude.service.Service.is_installed", return_value=True)
def test_claude_cli_info_works(
    mock_has_config,
    mock_process_iter,
    mock_platform,
    runner,
) -> None:
    """Check info spots spots installed and running Claude."""
    mock_process = Mock()
    mock_process.info = {
        "pid": 1234,
        "ppid": 0,
        "name": "Claude",
    }
    mock_process.cmdline = lambda: [
        "/Applications/Claude.app/Contents/MacOS/Claude",
        "--annotation=_productName=Claude",
    ]
    mock_process_iter.return_value = [mock_process]

    result = runner.invoke(cli, ["claude", "info"])
    assert result.exit_code == 0
    info = json.loads(result.stdout)
    assert info["is_installed"] is True
    assert info["is_running"] is True


def test_claude_cli_config_works(runner, tmp_path) -> None:
    """Check config works."""
    # Set up test config file in isolated tmp directory
    config_dir = tmp_path / "Claude"
    config_dir.mkdir()
    config_file = config_dir / "claude_desktop_config.json"
    test_config = {"mcpServers": {"starbridge": {"command": "uv"}}}
    config_file.write_text(json.dumps(test_config))

    with patch(
        "starbridge.claude.service.Service.application_directory",
        return_value=config_dir,
    ):
        result = runner.invoke(cli, ["claude", "config"])

        assert result.exit_code == 0
        assert '"mcpServers"' in result.stdout
        assert '"starbridge"' in result.stdout


@patch("starbridge.claude.service.Service.is_installed", return_value=False)
def test_claude_cli_config_fails_if_not_installed(mock_is_installed, runner) -> None:
    """Check config fails when config path is not a file."""
    result = runner.invoke(cli, ["claude", "config"])
    assert result.exit_code == 0
    assert "not installed" in result.stdout


@patch("starbridge.claude.service.Service.is_installed", return_value=True)
@patch(
    "starbridge.claude.service.Service.config_path",
    return_value=Path("/nonexistent/config.json"),
)
def test_claude_cli_config_fails_if_no_config(
    mock_is_installed,
    mock_config_path,
    runner,
) -> None:
    """Check config fails when no config file."""
    result = runner.invoke(cli, ["claude", "config"])
    assert result.exit_code == 0
    assert "No config" in result.stdout


def test_claude_cli_log_works(runner, tmp_path, capfd) -> None:
    """Check showing log works."""
    # Set up test config file in isolated tmp directory
    log_dir = tmp_path / "Claude"
    log_dir.mkdir()
    main_log_file = log_dir / "mcp.log"
    main_log_file.write_text("claude\n")
    starbridge_log_file = log_dir / "mcp-server-starbridge.log"
    starbridge_log_file.write_text("starbridge\n")

    with patch(
        "starbridge.claude.service.Service.log_directory",
        return_value=log_dir,
    ):
        result = runner.invoke(cli, ["claude", "log", "--name", "main"])
        assert result.exit_code == 0
        out, _ = capfd.readouterr()
        assert "claude" in out
        result = runner.invoke(cli, ["claude", "log"])
        assert result.exit_code == 0
        out, _ = capfd.readouterr()
        assert "starbridge" in out


@patch("starbridge.claude.service.Service.is_installed", return_value=False)
def test_claude_cli_restart_fails_if_not_installed(mock_is_installed, runner) -> None:
    """Check restart fails if Claude not installed."""
    result = runner.invoke(cli, ["claude", "restart"])
    assert result.exit_code == 0
    assert "not installed" in result.stdout


@patch("starbridge.claude.service.Service.is_installed", return_value=True)
@patch("psutil.process_iter")
@patch("subprocess.run", return_value=subprocess.CompletedProcess([], 0))
def test_claude_cli_restart_works_if_installed(
    mock_subprocess_run,
    mock_process_iter,
    mock_is_installed,
    runner,
) -> None:
    """Check restart works on supported platforms."""
    mock_process_claude = Mock()
    mock_process_claude.info = {"name": "Claude"}
    mock_process_other = Mock()
    mock_process_other.info = {"name": "Other"}
    mock_process_iter.return_value = [mock_process_other, mock_process_claude]

    platform_commands = {
        "Darwin": {"args": ["/usr/bin/open", "-a", "Claude"], "shell": False},
        "win23": {"args": ["start", "Claude"], "shell": True},
        "Linux": {"args": ["xdg-open", "Claude"], "shell": False},
    }

    for platform_name, command in platform_commands.items():
        with patch("platform.system", return_value=platform_name):
            result = runner.invoke(cli, ["claude", "restart"])
            mock_process_claude.terminate.assert_called_once()
            assert mock_process_other.terminate.call_count == 0
            mock_subprocess_run.assert_called_once_with(
                command["args"],
                shell=command["shell"],
                check=True,
            )
            assert result.exit_code == 0
            assert "was restarted" in result.stdout
            mock_process_claude.reset_mock()
            mock_subprocess_run.reset_mock()


@patch("starbridge.claude.service.Service.is_installed", return_value=True)
@patch("psutil.process_iter")
@patch("subprocess.run", return_value=subprocess.CompletedProcess([], 0))
def test_claude_cli_restart_fails_on_unknown_system(
    mock_subprocess_run,
    mock_process_iter,
    mock_is_installed,
    runner,
) -> None:
    """Check restart fails if Claude running on unknown platform."""
    mock_process = Mock()
    mock_process.info = {"name": "Claude"}
    mock_process_iter.return_value = [mock_process]

    with patch("platform.system", return_value="AmigaOS"):
        result = runner.invoke(cli, ["claude", "restart"])
        mock_process.terminate.assert_called_once()
        assert result.exit_code == 1
        assert mock_subprocess_run.called is False
        mock_process.reset_mock()
        mock_subprocess_run.reset_mock()


@patch("starbridge.claude.service.Service.is_installed", return_value=True)
@patch(
    "starbridge.claude.service.Service.platform_supports_restart",
    return_value=False,
)  # TODO(@helmut-hoffer-von-ankershoffen): find out why we cannot patch is_running_in_container
def test_claude_cli_restart_fails_in_container(
    mock_platform_supports_restart,
    mock_is_installed,
    runner,
) -> None:
    """Check restart fails if Claude running in container."""
    result = runner.invoke(cli, ["claude", "restart"])
    assert result.exit_code == 1


def test_claude_cli_in_container_commands_not_available() -> None:
    """Check log command not available in container."""
    env = os.environ.copy()
    env.update({
        "COVERAGE_PROCESS_START": "pyproject.toml",
        "COVERAGE_FILE": os.getenv("COVERAGE_FILE", ".coverage"),
        "STARBRIDGE_RUNNING_IN_CONTAINER": "1",  # indicate we are running within a container
    })
    # Test commands not available in container
    for command in ["log", "restart", "config"]:
        result = subprocess.run(
            ["uv", "run", "starbridge", "claude", command],
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )
        assert result.returncode == 2
        assert "No such command" in result.stderr
