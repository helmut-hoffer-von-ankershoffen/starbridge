import os
import pathlib
import sys
from typing import Annotated, Any

import typer
from dotenv import dotenv_values
from rich.prompt import Prompt

import starbridge.claude
import starbridge.mcp
from starbridge.base import __project_name__, __version__
from starbridge.mcp import MCPBaseService, MCPServer
from starbridge.utils import console, get_logger, get_process_info

# Initializes logging and instrumentation
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
    for service_class in MCPBaseService.get_services():
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


@cli.command()
def install(
    atlassian_url: Annotated[
        str,
        typer.Option(
            prompt="Base url of your Confluence and Jira installation",
            help="Base url of your Confluence and Jira installation, e.g. https://your-domain.atlassian.net",
        ),
    ] = os.environ.get("STARBRIDGE_ATLASSIAN_URL", "https://your-domain.atlassian.net"),
    atlassian_email_address: Annotated[
        str,
        typer.Option(
            prompt="Email address of your Atlassian account",
            help="Email address of your Atlassian account, e.g. you@your-domain.com",
        ),
    ] = os.environ.get("STARBRIDGE_ATLASSIAN_EMAIL_ADDRESS", "you@your-domain.com"),
    atlassian_api_token: Annotated[
        str,
        typer.Option(
            prompt="Go to https://id.atlassian.com/manage-profile/security/api-tokens to create an API token for starbridge",
            help="API token of your Atlassian account, go to https://id.atlassian.com/manage-profile/security/api-tokens to create one",
        ),
    ] = os.environ.get("STARBRIDGE_ATLASSIAN_API_TOKEN", "YOUR_TOKEN"),
    restart_claude: Annotated[
        bool,
        typer.Option(
            help="Restart Claude Desktop application post installation",
        ),
    ] = starbridge.claude.Service.platform_supports_restart(),
    image: Annotated[
        str,
        typer.Option(
            help="Docker image to use for Starbridge. Only applies if started as container.",
        ),
    ] = "helmuthva/starbridge:latest",
):
    """Install starbridge within Claude Desktop application by adding to configuration and restarting Claude Desktop app"""
    if starbridge.claude.Service.install_mcp_server(
        _generate_mcp_server_config(
            atlassian_url, atlassian_email_address, atlassian_api_token, image
        ),
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
    ] = starbridge.claude.Service.platform_supports_restart(),
):
    """Install starbridge from Claude Desktop application by removing from configuration and restarting Claude Desktop app"""
    if starbridge.claude.Service.uninstall_mcp_server(restart=restart_claude):
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
    atlassian_url: str,
    atlassian_email_address: str,
    atlassian_api_token: str,
    image: str = "helmuthva/starbridge:latest",
) -> dict:
    """Generate configuration file for Starbridge"""
    env = {
        "STARBRIDGE_ATLASSIAN_URL": atlassian_url,
        "STARBRIDGE_ATLASSIAN_EMAIL_ADDRESS": atlassian_email_address,
        "STARBRIDGE_ATLASSIAN_API_TOKEN": atlassian_api_token,
    }
    if starbridge.claude.Service.is_running_in_starbridge_container():
        return {
            "command": "docker",
            "args": [
                "run",
                "-i",
                "--rm",
                "-e",
                "STARBRIDGE_ATLASSIAN_URL",
                "-e",
                "STARBRIDGE_ATLASSIAN_EMAIL_ADDRESS",
                "-e",
                "STARBRIDGE_ATLASSIAN_API_TOKEN",
                image,
            ],
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


cli.add_typer(
    starbridge.mcp.cli,
    name="mcp",
    help="MCP operations",
)

for service_class in MCPBaseService.get_services():
    name, typer_cli = service_class.get_cli()
    if name and typer_cli:
        cli.add_typer(
            typer_cli,
            name=name,
            help=f"{name.title()} operations",
        )


def _add_epilog_recursively(cli: typer.Typer):
    """Add epilog to all typers in the tree"""
    cli.info.epilog = f"⭐ Starbridge v{__version__}: built with love in Berlin 🐻"
    for group in cli.registered_groups:
        if isinstance(group, typer.models.TyperInfo):
            typer_instance = group.typer_instance
            if (typer_instance is not cli) and typer_instance:
                _add_epilog_recursively(typer_instance)
    for command in cli.registered_commands:
        if isinstance(command, typer.models.CommandInfo):
            command.epilog = cli.info.epilog


_add_epilog_recursively(cli)


def _no_args_is_help_recursively(cli: typer.Typer):
    """Add epilog to all typers in the tree"""
    for group in cli.registered_groups:
        if isinstance(group, typer.models.TyperInfo):
            group.no_args_is_help = True
            typer_instance = group.typer_instance
            if (typer_instance is not cli) and typer_instance:
                _no_args_is_help_recursively(typer_instance)


_no_args_is_help_recursively(cli)


if __name__ == "__main__":
    try:
        cli()
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Fatal error occurred: {e}")
        console.print(f"Fatal error occurred: {e}", style="error")
        sys.exit(1)
