import os
import shutil
from pathlib import Path

import pytest
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


def test_dot_env(runner):
    """Check missing entry in .env leads to validation error."""

    result = runner.invoke(cli, ["health"])
    assert result.exit_code == 0

    # Read .env, remove STARBRIDGE_ATLASSIAN_URL line and write back
    env_path = Path(__file__).parent.parent / ".env"
    with open(env_path) as f:
        lines = f.readlines()

    with open(env_path, "w") as f:
        for line in lines:
            if not line.startswith("STARBRIDGE_ATLASSIAN_URL"):
                f.write(line)
    os.environ.pop("STARBRIDGE_ATLASSIAN_URL", None)

    result = runner.invoke(cli, ["health"])
    assert result.exit_code == 78
    assert "STARBRIDGE_ATLASSIAN_URL: Field required" in result.output
