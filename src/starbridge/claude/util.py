"""Utility functions for Claude Desktop application integration."""

from typing import Any

from starbridge import (
    __is_development_mode__,
    __is_running_in_container__,
    __project_name__,
    __project_path__,
)


def generate_mcp_server_config(
    env: dict[str, Any],
    image: str = "helmuthva/starbridge:latest",
) -> dict:
    """
    Generate configuration file for Starbridge.

    Returns:
        dict: Generated configuration data.

    """
    if __is_running_in_container__:
        args = ["run", "-i", "--rm"]
        for env_key in env:
            args.extend(["-e", env_key])
        args.append(image)
        return {
            "command": "docker",
            "args": args,
            "env": env,
        }
    if __is_development_mode__:
        return {
            "command": "uv",
            "args": [
                "--directory",
                __project_path__,
                "run",
                "--no-dev",
                __project_name__,
            ],
            "env": env,
        }
    return {
        "command": "uvx",
        "args": [
            __project_name__,
        ],
        "env": env,
    }
