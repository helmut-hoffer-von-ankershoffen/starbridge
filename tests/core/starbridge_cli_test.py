import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from starbridge import __version__
from starbridge.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_built_with_love(runner):
    """Check epilog shown."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "built with love in Berlin" in result.output


def test_cli_invalid_command(runner):
    """Test invalid command returns error"""
    result = runner.invoke(cli, ["invalid"])
    assert result.exit_code != 0


def test_cli_info(runner):
    """Check processes exposed and version matching."""
    result = runner.invoke(cli, ["info"])
    assert result.exit_code == 0
    assert "'pid'" in result.stdout
    assert f"'version': '{__version__}'" in result.stdout


def test_cli_create_dot_env(runner, tmp_path):
    """Check configuration injected in claude as expected."""
    with runner.isolated_filesystem():
        inputs = (
            "https://test.atlassian.net\n"
            "test@test.com\n"  # Atlassian email address
            "TEST_CONFLUENCE_API_TOKEN\n"  # Atlassian token
            "TEST_LOGFIRE_TOKEN\n"  # logfire token
            "production\n"  # logfire environment
            "1\n"  # instrument mcp server
            "INFO\n"  # log level
            "1\n"  # log to file
            "test.log\n"  # log file
            "0\n"  # log to console
            "TEST_USER_AGENT\n"  # custom user agent
        )
        result = runner.invoke(cli, ["create-dot-env"], input=inputs)
        assert result.exit_code == 0
        dot_env = Path(".env").read_text()
        assert "STARBRIDGE_ATLASSIAN_URL=https://test.atlassian.net" in dot_env
        assert "STARBRIDGE_ATLASSIAN_EMAIL_ADDRESS=test@test.com" in dot_env
        assert "STARBRIDGE_ATLASSIAN_API_TOKEN=TEST_CONFLUENCE_API_TOKEN" in dot_env
        assert "STARBRIDGE_LOGFIRE_TOKEN=TEST_LOGFIRE_TOKEN" in dot_env
        assert "STARBRIDGE_LOGFIRE_ENVIRONMENT=production" in dot_env
        assert "STARBRIDGE_LOGFIRE_INSTRUMENT_MCP_ENABLED=1" in dot_env
        assert "STARBRIDGE_LOGGING_LOGLEVEL=INFO" in dot_env
        assert "STARBRIDGE_LOGGING_LOG_FILE_ENABLED=1" in dot_env
        assert "STARBRIDGE_LOGGING_LOG_FILE_NAME=test.log" in dot_env
        assert "STARBRIDGE_LOGGING_LOG_CONSOLE_ENABLED=0" in dot_env
        assert "STARBRIDGE_WEB_USER_AGENT=TEST_USER_AGENT" in dot_env


def test_cli_install(runner, tmp_path):
    """Check configuration injected in claude as expected."""
    with patch(
        "starbridge.claude.service.Service.application_directory", return_value=tmp_path
    ):
        inputs = (
            "https://test.atlassian.net\n"
            "test@test.com\n"  # Atlassian email address
            "TEST_CONFLUENCE_API_TOKEN\n"  # Atlassian token
            "TEST_LOGFIRE_TOKEN\n"  # logfire token
            "production\n"  # logfire environment
            "1\n"  # instrument mcp server
            "INFO\n"  # log level
            "1\n"  # log to file
            "test.log\n"  # log file
            "0\n"  # log to console
            "TEST_USER_AGENT\n"  # custom user agent
        )
        result = runner.invoke(cli, ["install", "--no-restart-claude"], input=inputs)
        assert result.exit_code == 0

        result = runner.invoke(cli, ["claude", "config"], input=inputs)
        assert result.exit_code == 0
        # Find start of JSON by looking for first '{'
        json_start = result.output.find("{")
        output_json = json.loads(result.output[json_start:])
        server_config = output_json["mcpServers"]["starbridge"]
        assert (
            server_config["env"]["STARBRIDGE_ATLASSIAN_URL"]
            == "https://test.atlassian.net"
        )
        assert (
            server_config["env"]["STARBRIDGE_ATLASSIAN_EMAIL_ADDRESS"]
            == "test@test.com"
        )
        assert (
            server_config["env"]["STARBRIDGE_ATLASSIAN_API_TOKEN"]
            == "TEST_CONFLUENCE_API_TOKEN"
        )

        result = runner.invoke(cli, ["uninstall", "--no-restart-claude"], input=inputs)
        assert result.exit_code == 0

        result = runner.invoke(cli, ["claude", "config"], input=inputs)
        assert result.exit_code == 0
        json_start = result.output.find("{")
        output_json = json.loads(result.output[json_start:])
        assert output_json["mcpServers"].get("starbridge") is None


def test_cli_main_guard():
    env = os.environ.copy()
    env.update({
        "COVERAGE_PROCESS_START": "pyproject.toml",
        "COVERAGE_FILE": os.getenv("COVERAGE_FILE", ".coverage"),
    })
    result = subprocess.run(
        [sys.executable, "-m", "starbridge.cli", "hello", "hello"],
        capture_output=True,
        text=True,  # Get string output instead of bytes
        env=env,
    )
    assert result.returncode == 0
    assert "Hello World!" in result.stdout


def test_cli_main_guard_fail():
    env = os.environ.copy()
    env.update({
        "COVERAGE_PROCESS_START": "pyproject.toml",
        "COVERAGE_FILE": os.getenv("COVERAGE_FILE", ".coverage"),
        "MOCKS": "starbridge_hello_service_hello_fail",
    })
    result = subprocess.run(
        [sys.executable, "-m", "starbridge.cli", "hello", "hello"],
        capture_output=True,
        text=True,
        env=env,  # Get string output instead of bytes
    )
    assert result.returncode == 1
    assert "Fatal error occurred: Hello World failed" in result.stdout
