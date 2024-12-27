import os
import pathlib
import sys
from typing import Annotated, Any

import typer
from dotenv import dotenv_values
from pydantic import SecretStr
from pydantic_settings import BaseSettings
from rich.prompt import Prompt

from starbridge.base import __project_name__, __version__
from starbridge.claude import Service as ClaudeService
from starbridge.mcp import MCPServer
from starbridge.utils import (
    add_epilog_recursively,
    console,
    get_logger,
    get_process_info,
    locate_implementations,
    locate_subclasses,
    no_args_is_help_recursively,
)

logger = get_logger(__name__)

cli = typer.Typer(
    name="Starbridge CLI",
)


@cli.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    host: Annotated[
        str | None,
        typer.Option(
            help="Host to run the server on",
        ),
    ] = None,
    port: Annotated[
        int | None,
        typer.Option(
            help="Port to run the server on",
        ),
    ] = None,
    debug: Annotated[
        bool,
        typer.Option(
            help="Debug mode",
        ),
    ] = True,
    env: Annotated[  # Parsed in bootstrap.py
        list[str] | None,
        typer.Option(
            "--env",
            help='Environment variables in key=value format. Can be used multiple times in one call. Only STARBRIDGE_ prefixed vars are used. Example --env STARBRIDGE_ATLASSIAN_URL="https://your-domain.atlassian.net" --env STARBRIDGE_ATLASSIAN_EMAIL="YOUR_EMAIL"',
        ),
    ] = None,
):
    """Run MCP Server - alias for 'mcp serve'"""
    # Environment variables are handled in bootstrap
    if ctx.invoked_subcommand is None:
        MCPServer.serve(host, port, debug)


@cli.command()
def health(json: Annotated[bool, typer.Option(help="Output health as JSON")] = False):
    """Check health of services and their dependencies."""
    health = MCPServer().health()
    if not health.healthy:
        logger.warning(f"health: {health}")
    if json:
        console.print(health.model_dump_json())
    else:
        console.print(health)


@cli.command()
def info():
    """Info about Starbridge and it's environment"""
    data: dict[str, Any] = {
        "version": __version__,
        "path": _get_starbridge_path(),
        "development_mode": _is_development_mode(),
        "env": _get_starbridge_env(),
        "process": get_process_info().model_dump(),
    }

    # Auto-discover and get info from all services
    for service_class in MCPServer.service_classes():
        service = service_class()
        service_name = service.__class__.__module__.split(".")[1]
        data[service_name] = service.info()

    console.print(data)
    logger.debug(data)


@cli.command()
def configure():
    """Generate .env file for Starbridge"""
    if not _is_development_mode():
        raise RuntimeError("This command is only available in development mode")

    starbridge_path = pathlib.Path(_get_starbridge_path())
    env_example_path = starbridge_path / ".env.example"
    env_path = starbridge_path / ".env"

    if not env_example_path.exists():
        raise FileNotFoundError(
            f"Required .env.example file not found at {env_example_path}"
        )

    example_values = dotenv_values(env_example_path)
    current_values = dotenv_values(env_path) if env_path.exists() else {}

    new_values = {}
    for key in example_values:
        default_value = current_values.get(key, example_values[key])
        value = Prompt.ask(
            f"Enter value for {key}",
            default=default_value if default_value else None,
            password="TOKEN" in key or "SECRET" in key,
        )
        new_values[key] = value

    with open(env_path, "w") as f:
        for key, value in new_values.items():
            # Try to convert to number, if it fails, it's not a number
            try:
                float(value)
                f.write(f"{key}={value}\n")
            except ValueError:
                f.write(f'{key}="{value}"\n')


def _collect_settings() -> dict[str, Any]:
    """Collect settings from user input for all BaseSettings subclasses"""
    prompted_settings = {}
    for settings in locate_subclasses(BaseSettings):
        settings_instance = settings()
        for field_name, field in settings.model_fields.items():
            description = field.description or field_name
            example = field.examples[0] if field.examples else None
            description = f"{description} (e.g. {example})" if example else description
            default_value = getattr(settings_instance, field_name, None)
            value = Prompt.ask(
                description,
                default=str(default_value) if default_value else None,
                password=isinstance(field.annotation, type(SecretStr)),
            )
            field_prefix = settings.model_config.get("env_prefix", "")
            prompted_settings[f"{field_prefix}{field_name.upper()}"] = value
    return prompted_settings


@cli.command()
def install(
    restart_claude: Annotated[
        bool,
        typer.Option(
            help="Restart Claude Desktop application post installation",
        ),
    ] = ClaudeService.platform_supports_restart(),
    image: Annotated[
        str,
        typer.Option(
            help="Docker image to use for Starbridge. Only applies if started as container.",
        ),
    ] = "helmuthva/starbridge:latest",
):
    """Install starbridge within Claude Desktop application by adding to configuration and restarting Claude Desktop app"""
    prompted_settings = _collect_settings()
    if ClaudeService.install_mcp_server(
        _generate_mcp_server_config(prompted_settings, image),
        restart=restart_claude,
    ):
        console.print("Starbridge installed with Claude Desktop application.")
        if not restart_claude:
            console.print(
                "Please restart Claude Desktop application to complete the installation."
            )
    else:
        console.print("Starbridge was already installed", style="warning")


@cli.command()
def uninstall(
    restart_claude: Annotated[
        bool,
        typer.Option(
            help="Restart Claude Desktop application post installation",
        ),
    ] = ClaudeService.platform_supports_restart(),
):
    """Install starbridge from Claude Desktop application by removing from configuration and restarting Claude Desktop app"""
    if ClaudeService.uninstall_mcp_server(restart=restart_claude):
        console.print("Starbridge uninstalled from Claude Destkop application.")
    else:
        console.print("Starbridge was no installed", style="warning")


def _is_development_mode():
    return "uvx" not in sys.argv[0].lower()


def _get_starbridge_path() -> str:
    return str(pathlib.Path(__file__).parent.parent.parent)


def _get_starbridge_env():
    """Get environment variables starting with STARBRIDGE_"""
    return {k: v for k, v in os.environ.items() if k.startswith("STARBRIDGE_")}


def _generate_mcp_server_config(
    prompted_settings: dict[str, Any],
    image: str = "helmuthva/starbridge:latest",
) -> dict:
    """Generate configuration file for Starbridge"""
    env = {key: str(value) for key, value in prompted_settings.items()}
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
    if _is_development_mode():
        return {
            "command": "uv",
            "args": [
                "--directory",
                _get_starbridge_path(),
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


# dynamically locate and register subcommands
for _cli in locate_implementations(typer.Typer):
    if _cli != cli:
        cli.add_typer(_cli)

# add epilog for all subcommands
add_epilog_recursively(
    cli, f"⭐ Starbridge v{__version__}: built with love in Berlin 🐻"
)

# add no_args_is_help for all subcommands
no_args_is_help_recursively(cli)

if __name__ == "__main__":
    try:
        cli()
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Fatal error occurred: {e}")
        console.print(f"Fatal error occurred: {e}", style="error")
        sys.exit(1)
