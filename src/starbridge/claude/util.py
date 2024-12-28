from typing import Any

from starbridge import __is_development_mode__, __project_name__, __project_path__

from .service import Service as ClaudeService


def generate_mcp_server_config(
    env: dict[str, Any],
    image: str = "helmuthva/starbridge:latest",
) -> dict:
    """Generate configuration file for Starbridge"""
    if ClaudeService.is_running_in_starbridge_container():
        args = ["run", "-i", "--rm"]
        for env_key in env.keys():
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
