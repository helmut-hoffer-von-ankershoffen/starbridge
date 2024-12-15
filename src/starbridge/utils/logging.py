import logging
import os

import click
import logfire
from rich.console import Console
from rich.logging import RichHandler


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

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"),
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[rich_handler, logfire.LogfireLoggingHandler()],
)

log = logging.getLogger()
