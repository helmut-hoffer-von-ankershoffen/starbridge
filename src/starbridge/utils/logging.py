import logging

import click
from rich.logging import RichHandler

from starbridge.utils.console import console


class CustomFilter(logging.Filter):
    def filter(self, record):
        return True


rich_handler = RichHandler(
    console=console,
    markup=True,
    rich_tracebacks=True,
    tracebacks_suppress=[click],
    show_path=True,
    show_level=True,
    enable_link_path=True,
)
rich_handler.addFilter(CustomFilter())

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[rich_handler],
)

log = logging.getLogger("rich")
