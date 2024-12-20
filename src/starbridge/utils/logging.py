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

    loglevel: Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"] = "INFO"
    log_file_enabled: bool = True
    log_file_name: str = "starbridge.log"
    log_console_enabled: bool = False


settings = load_settings(LoggingSettings)


class CustomFilter(logging.Filter):
    # TODO: Define what log lines you want to filter here
    def filter(self, record):
        return True


log_filter = CustomFilter()

handlers = []

if settings.log_file_enabled:
    file_handler = logging.FileHandler(settings.log_file_name)
    file_formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)
    file_handler.addFilter(log_filter)
    handlers.append(file_handler)

if settings.log_console_enabled:
    rich_handler = RichHandler(
        console=Console(stderr=True),
        markup=True,
        rich_tracebacks=True,
        tracebacks_suppress=[click],
        show_time=True,
        omit_repeated_times=True,
        show_path=True,
        show_level=True,
        enable_link_path=True,
    )
    rich_handler.addFilter(log_filter)
    handlers.append(rich_handler)

logfire_initialized = logfire_initialize()
if logfire_initialized:
    logfire_handler = logfire.LogfireLoggingHandler()
    logfire_handler.addFilter(log_filter)
    handlers.append(logfire_handler)


logging.basicConfig(
    level=settings.loglevel,
    format="%(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=handlers,
)
