import typer

from .di import (
    locate_implementations,
)


def prepare_cli(cli: typer.Typer, epilog: str):
    """Dynamically locate, register and prepare subcommands"""
    for _cli in locate_implementations(typer.Typer):
        if _cli != cli:
            cli.add_typer(_cli)

    # add epilog for all subcommands
    _add_epilog_recursively(cli, epilog)

    # add no_args_is_help for all subcommands
    _no_args_is_help_recursively(cli)


def _add_epilog_recursively(cli: typer.Typer, epilog: str):
    """Add epilog to all typers in the tree"""
    cli.info.epilog = epilog
    for group in cli.registered_groups:
        if isinstance(group, typer.models.TyperInfo):
            typer_instance = group.typer_instance
            if (typer_instance is not cli) and typer_instance:
                _add_epilog_recursively(typer_instance, epilog)
    for command in cli.registered_commands:
        if isinstance(command, typer.models.CommandInfo):
            command.epilog = cli.info.epilog


def _no_args_is_help_recursively(cli: typer.Typer):
    """Add epilog to all typers in the tree"""
    for group in cli.registered_groups:
        if isinstance(group, typer.models.TyperInfo):
            group.no_args_is_help = True
            typer_instance = group.typer_instance
            if (typer_instance is not cli) and typer_instance:
                _no_args_is_help_recursively(typer_instance)
