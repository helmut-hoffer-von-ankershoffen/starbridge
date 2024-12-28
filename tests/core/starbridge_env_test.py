import os
import shutil
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest
import typer
from typer.testing import CliRunner

from starbridge.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture(autouse=True)
def backup_env():
    """Fixture to automatically backup and restore .env file."""
    env_path = Path(__file__).parent.parent / ".env"
    bak_path = Path(__file__).parent.parent / ".env.bak"
    if env_path.is_file():
        shutil.copy2(env_path, bak_path)
    yield
    if bak_path.is_file():
        shutil.move(bak_path, env_path)


def test_env_args(runner):
    """Check --env can override environment for some commands."""

    def mock_asyncio_run(x):
        print("testing")
        raise typer.Exit(42)

    with patch("asyncio.run", side_effect=mock_asyncio_run):
        result = runner.invoke(
            cli,
            ["mcp", "serve", "--env", 'STARBRIDGE_ATLASSIAN_URL="https://test.com"'],
        )
    assert "testing" in result.output
    assert result.exit_code == 42

    with patch("asyncio.run", side_effect=mock_asyncio_run):
        result = runner.invoke(
            cli,
            ["--env", 'STARBRIDGE_ATLASSIAN_URL="https://test.com"'],
        )
    assert "testing" in result.output
    assert result.exit_code == 42


def test_env_args_fail(runner):
    """Check --env not supported for all commands."""

    result = subprocess.run(
        ["starbridge", "info", "--env", 'STARBRIDGE_LOG_LEVEL="DEBUG"'],
        capture_output=True,
        text=True,
    )
    assert "No such option" in result.stderr
    assert result.returncode == 2


@pytest.mark.sequential
def test_dot_env(runner):
    """Check missing entry in .env leads to validation error."""

    result = runner.invoke(cli, ["health"])
    assert result.exit_code == 0

    # Read .env, remove STARBRIDGE_ATLASSIAN_URL line and write back
    env_path = Path(__file__).parent.parent.parent / ".env"
    # Backup .env using Pathlib
    bak_path = Path(__file__).parent.parent.parent / ".env.bak"
    Path(bak_path).write_text(Path(env_path).read_text())

    with open(env_path) as f:
        lines = f.readlines()

    with open(env_path, "w") as f:
        for line in lines:
            if not line.startswith("STARBRIDGE_ATLASSIAN_URL"):
                f.write(line)
    os.environ.pop("STARBRIDGE_ATLASSIAN_URL", None)

    result = runner.invoke(cli, ["health"])
    Path(env_path).write_text(Path(bak_path).read_text())
    assert result.exit_code == 78
    assert "STARBRIDGE_ATLASSIAN_URL: Field required" in result.output
