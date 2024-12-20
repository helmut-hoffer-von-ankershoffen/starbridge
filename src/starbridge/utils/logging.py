import logging
from typing import Literal

import click
import logfire
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich.console import Console
from rich.logging import RichHandler

from starbridge.base import __project_name__
from starbridge.instrumentation import logfire_initialize
from starbridge.utils.settings import load_settings


def get_logger(name: str | None) -> logging.Logger:
    if (name is None) or (name == __project_name__):
        return logging.getLogger(__project_name__)
    return logging.getLogger(f"{__project_name__}.{name}")


class LoggingSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix=f"{__project_name__.upper()}_LOGGING_",
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    loglevel: Literal["FATAL", "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"] = "INFO"
    log_file_enabled: bool = True
    log_file_name: str = "starbridge.log"
    log_console_enabled: bool = False


settings = load_settings(LoggingSettings)

handlers = []

if settings.log_file_enabled:
    handlers.append(
        logging.FileHandler(settings.log_file_name),
    )

if settings.log_console_enabled:
    rich_handler = RichHandler(
        console=Console(stderr=True),
        markup=True,
        rich_tracebacks=True,
        tracebacks_suppress=[click],
        show_path=True,
        show_level=True,
        enable_link_path=True,
    )

    class CustomFilter(logging.Filter):
        def filter(self, record):
            return True

    rich_handler.addFilter(CustomFilter())
    handlers.append(rich_handler)

logfire_initialized = logfire_initialize()
if logfire_initialized:
    handlers.append(
        logfire.LogfireLoggingHandler(),
    )


logging.basicConfig(
    level=settings.loglevel,
    format="%(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=handlers,
)
