"""Tests for platform-specific functionality."""

import json
import os
import subprocess

from starbridge import __is_running_in_container__


def test_container_running_in_platform() -> None:
    """Check behavior of container running in platform."""
    assert not __is_running_in_container__

    env = os.environ.copy()
    env["STARBRIDGE_RUNNING_IN_CONTAINER"] = "1"

    result = subprocess.run(
        ["uv", "run", "starbridge", "info"],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )

    info = json.loads(result.stdout)
    assert info["is_running_in_container"] is True
