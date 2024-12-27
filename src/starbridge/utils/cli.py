import typer

from starbridge.base import __version__


def add_epilog_recursively(cli: typer.Typer, epilog: str):
    """Add epilog to all typers in the tree"""
    cli.info.epilog = epilog
    for group in cli.registered_groups:
        if isinstance(group, typer.models.TyperInfo):
            typer_instance = group.typer_instance
            if (typer_instance is not cli) and typer_instance:
                add_epilog_recursively(typer_instance, epilog)
    for command in cli.registered_commands:
        if isinstance(command, typer.models.CommandInfo):
            command.epilog = cli.info.epilog


def no_args_is_help_recursively(cli: typer.Typer):
    """Add epilog to all typers in the tree"""
    for group in cli.registered_groups:
        if isinstance(group, typer.models.TyperInfo):
            group.no_args_is_help = True
            typer_instance = group.typer_instance
            if (typer_instance is not cli) and typer_instance:
                no_args_is_help_recursively(typer_instance)
