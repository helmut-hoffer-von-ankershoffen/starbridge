"""Tests for core environment handling."""

import os
import shutil
import subprocess
import sys
from collections.abc import Generator
from pathlib import Path
from typing import Never
from unittest.mock import patch

import pytest
import typer
from typer.testing import CliRunner

from starbridge.cli import cli


@pytest.fixture
def runner() -> CliRunner:
    """Get a Click CLI test runner."""
    return CliRunner()


@pytest.fixture(autouse=True)
def backup_env() -> Generator[None, None, None]:
    """Fixture to automatically backup and restore .env file."""
    env_path = Path(__file__).parent.parent / ".env"
    bak_path = Path(__file__).parent.parent / ".env.bak"
    if env_path.is_file():
        shutil.copy2(env_path, bak_path)
    yield
    if bak_path.is_file():
        shutil.move(bak_path, env_path)


def test_core_env_args_passed(runner) -> None:
    """Check --env can override environment for some commands."""

    def mock_asyncio_run(x) -> Never:
        raise typer.Exit(42)

    with patch("asyncio.run", side_effect=mock_asyncio_run):
        result = runner.invoke(
            cli,
            [
                "mcp",
                "serve",
                "--env",
                'STARBRIDGE_ATLASSIAN_URL="https://test.com"',
                "--env",
                "OTHER_ENV=4711",
                "--env",
                "VALUE_ERROR",
            ],
        )
        assert result.exit_code == 42

    with patch("asyncio.run", side_effect=mock_asyncio_run):
        result = runner.invoke(
            cli,
            ["--env", 'STARBRIDGE_ATLASSIAN_URL="https://test.com"'],
        )
        assert result.exit_code == 42


def test_core_env_args_fail(runner) -> None:
    """Check --env not supported for all commands."""
    result = subprocess.run(
        ["starbridge", "info", "--env", 'STARBRIDGE_LOG_LEVEL="DEBUG"'],
        capture_output=True,
        text=True,
        check=False,
    )
    assert "No such option" in result.stderr
    assert result.returncode == 2


@pytest.mark.sequential
def test_core_dot_env_validated(runner) -> None:
    """Check missing entry in .env leads to validation error."""
    result = runner.invoke(cli, ["health"])
    assert result.exit_code == 0

    # Read .env, remove STARBRIDGE_ATLASSIAN_URL line and write back
    env_path = Path(__file__).parent.parent.parent / ".env"
    # Backup .env using Pathlib
    bak_path = Path(__file__).parent.parent.parent / ".env.bak"
    Path(bak_path).write_text(Path(env_path).read_text(encoding="utf-8"), encoding="utf-8")

    with open(env_path, encoding="utf-8") as f:
        lines = f.readlines()

    with open(env_path, "w", encoding="utf-8") as f:
        for line in lines:
            if not line.startswith("STARBRIDGE_ATLASSIAN_URL"):
                f.write(line)
    os.environ.pop("STARBRIDGE_ATLASSIAN_URL", None)

    result = runner.invoke(cli, ["health"])
    Path(env_path).write_text(Path(bak_path).read_text(encoding="utf-8"), encoding="utf-8")
    assert result.exit_code == 78
    assert "STARBRIDGE_ATLASSIAN_URL: Field required" in result.output


def test_parse_env_args() -> None:
    """Test parsing of environment variables from command line arguments."""
    from starbridge import _parse_env_args

    original_argv = sys.argv
    original_env = os.environ.copy()

    try:
        # Test valid STARBRIDGE_ prefixed vars
        sys.argv = [
            "starbridge",
            "--env",
            'STARBRIDGE_TEST="value"',
            "-e",
            "STARBRIDGE_OTHER=123",
            "--env",
            'STARBRIDGE_QUOTED="quoted value"',
        ]
        _parse_env_args()
        assert os.environ["STARBRIDGE_TEST"] == "value"
        assert os.environ["STARBRIDGE_OTHER"] == "123"
        assert os.environ["STARBRIDGE_QUOTED"] == "quoted value"

        # Test non-STARBRIDGE vars are ignored
        sys.argv = ["starbridge", "--env", "OTHER_VAR=ignored"]
        _parse_env_args()
        assert "OTHER_VAR" not in os.environ

        # Test malformed vars are skipped
        sys.argv = ["starbridge", "--env", "STARBRIDGE_INVALID"]
        _parse_env_args()
        assert "STARBRIDGE_INVALID" not in os.environ

    finally:
        sys.argv = original_argv
        os.environ.clear()
        os.environ.update(original_env)
