import logging
from typing import Literal

import click
import logfire
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich.console import Console
from rich.logging import RichHandler

from starbridge.base import __project_name__, __version__
from starbridge.utils.settings import load_settings


class LoggingSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix=f"{__project_name__.upper()}_LOGGING_",
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    loglevel: Literal["FATAL", "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"] = "INFO"
    log_console: bool = False

    logfire_token: str | None = None
    logfire_environment: str = "default"


settings = load_settings(LoggingSettings)

logfire.configure(
    send_to_logfire="if-token-present",
    token=settings.logfire_token,
    environment=settings.logfire_environment,
    service_name=__project_name__,
    console=False,
    code_source=logfire.CodeSource(
        repository="https://github.com/helmut-hoffer-von-ankershoffen/starbridge",
        revision=__version__,
        root_path="",  # FIXME: root_path
    ),
)
logfire.instrument_system_metrics(base="full")
logfire.install_auto_tracing(
    modules=["starbridge.confluence"], min_duration=0.001
)  # FIXME: get modules from settings


class CustomFilter(logging.Filter):
    def filter(self, record):
        return True


rich_handler = RichHandler(
    console=Console(stderr=True),
    markup=True,
    rich_tracebacks=True,
    tracebacks_suppress=[click],
    show_path=True,
    show_level=True,
    enable_link_path=True,
)
rich_handler.addFilter(CustomFilter())

handlers = []
if settings.log_console:
    handlers.append(rich_handler)
handlers.extend([
    logging.FileHandler("starbridge.log"),
    logfire.LogfireLoggingHandler(),
])

logging.basicConfig(
    level=settings.loglevel,
    format="%(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=handlers,
)


def get_logger(name: str | None) -> logging.Logger:
    if (name is None) or (name == __project_name__):
        return logging.getLogger(__project_name__)
    return logging.getLogger(f"{__project_name__}.{name}")
