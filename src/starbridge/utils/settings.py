"""Utilities around Pydantic settings."""

import json
import logging
import os
from pathlib import Path
from typing import Any, TypeVar

from dotenv.cli import get
from pydantic import SecretStr, ValidationError
from pydantic_settings import BaseSettings
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

from starbridge.base import __project_name__
from starbridge.utils.console import console
from starbridge.utils.di import locate_subclasses

T = TypeVar("T", bound=BaseSettings)

logger = logging.getLogger(__name__)


def load_settings(settings_class: type[T]) -> T:
    """Load settings with error handling and nice formatting.

    Args:
        settings_class: The Pydantic settings class to instantiate

    Returns:
        (T): Instance of the settings class

    Raises:
        SystemExit: If settings validation fails
    """
    try:
        return settings_class()
    except ValidationError as e:
        errors = json.loads(e.json())
        text = Text()
        text.append(
            "Validation error(s): \n\n",
            style="debug",
        )

        prefix = settings_class.model_config.get("env_prefix", "")
        for error in errors:
            env_var = f"{prefix}{error['loc'][0]}".upper()
            logger.fatal(f"Configuration invalid! {env_var}: {error['msg']}")
            text.append(f"• {env_var}", style="yellow bold")
            text.append(f": {error['msg']}\n")

        text.append(
            "\nCheck settings defined in the process environment and in file ",
            style="info",
        )
        env_file = str(settings_class.model_config.get("env_file", ".env") or ".env")
        text.append(
            str(Path(__file__).parent.parent.parent.parent / env_file),
            style="bold blue underline",
        )

        console.print(
            Panel(
                text,
                title="Configuration invalid!",
                border_style="error",
            )
        )
        exit(78)


def _get_field_description(field_name: str, field: Any) -> str:
    """Generate description for a field with optional example."""
    description = field.description or field_name
    example = field.examples[0] if field.examples else None
    return f"{description} (e.g. {example})" if example else description


def _get_settings_instance(settings_set: type[BaseSettings]) -> BaseSettings:
    """Get settings instance with fallback to model_construct."""
    try:
        return settings_set()
    except ValidationError:
        return settings_set.model_construct()


def _transform_value(value: Any) -> str:
    """Transform a value to its string representation."""
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, SecretStr):
        return value.get_secret_value()
    return str(value)


def prompt_for_env() -> dict[str, Any]:
    """Collect settings from user input for all BaseSettings subclasses"""
    _input = {}
    for settings_set in locate_subclasses(BaseSettings):
        settings = _get_settings_instance(settings_set)
        field_prefix = settings.model_config.get("env_prefix", "")

        for field_name, field in settings.model_fields.items():
            description = _get_field_description(field_name, field)
            default_value = getattr(settings, field_name, None)
            is_bool = field.annotation is bool
            is_secret = field.annotation is SecretStr
            if is_bool:
                prompt_default = "1" if default_value else "0"
            else:
                if (default_value) and hasattr(default_value, "get_secret_value"):
                    prompt_default = default_value.get_secret_value()
                else:
                    prompt_default = str(default_value) if default_value else None
            while True:
                value = Prompt.ask(
                    description,
                    default=prompt_default,
                    password=False,
                    choices=["0", "1"] if is_bool else None,
                )
                try:
                    settings.__pydantic_validator__.validate_assignment(
                        settings.model_construct(), field_name, value
                    )
                    break
                except ValidationError as e:
                    console.print(f"[red]{e.errors()[0]['msg']}[/red]")

            key = f"{field_prefix}{field_name.upper()}"
            _input[key] = value

    return {key: _transform_value(value) for key, value in _input.items()}


def get_starbridge_env():
    return {
        k: v for k, v in os.environ.items() if k.startswith(__project_name__.upper())
    }
