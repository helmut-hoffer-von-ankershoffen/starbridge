import json
import os
import subprocess
import sys
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from starbridge.base import __version__
from starbridge.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_built_with_love(runner):
    """Check epilog shown."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "built with love in Berlin" in result.output


def test_invalid_command(runner):
    """Test invalid command returns error"""
    result = runner.invoke(cli, ["invalid"])
    assert result.exit_code != 0


def test_info(runner):
    """Check processes exposed and version matching."""
    result = runner.invoke(cli, ["info"])
    assert result.exit_code == 0
    assert "'uv'" in result.stdout
    assert f"'version': '{__version__}'" in result.stdout


def test_install(runner, tmp_path):
    """Check processes exposed and version matching."""
    with patch(
        "starbridge.claude.service.Service.application_directory", return_value=tmp_path
    ):
        inputs = (
            "https://your-domain.atlassian.net/test\n"
            "you-test@your-domain.com\n"  # Atlassian email address
            "YOUR_TEST_API_TOKEN\n"  # Atlassian token
            "\n"  # Possibly other prompt input
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
            == "https://your-domain.atlassian.net/test"
        )
        assert (
            server_config["env"]["STARBRIDGE_ATLASSIAN_EMAIL_ADDRESS"]
            == "you-test@your-domain.com"
        )
        assert (
            server_config["env"]["STARBRIDGE_ATLASSIAN_API_TOKEN"]
            == "YOUR_TEST_API_TOKEN"
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
