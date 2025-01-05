"""Test utility functions of the Starbridge package."""

import os

from mcp import StdioServerParameters
from mcp.client.stdio import get_default_environment

PYPROJECT_TOML = "pyproject.toml"
DOT_COVERAGE = ".coverage"


def _server_parameters(mocks: list[str] | None = None) -> StdioServerParameters:
    """Create server parameters with coverage enabled."""
    env = dict(get_default_environment())
    # Add coverage config to subprocess
    env.update({
        "COVERAGE_PROCESS_START": PYPROJECT_TOML,
        "COVERAGE_FILE": os.getenv("COVERAGE_FILE", DOT_COVERAGE),
    })
    if (mocks is not None) and mocks:
        env.update({"MOCKS": ",".join(mocks)})

    return StdioServerParameters(
        command="uv",
        args=["run", "starbridge"],
        env=env,
    )
