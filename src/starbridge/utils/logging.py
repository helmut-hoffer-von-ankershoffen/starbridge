import logging
import os

import click
import logfire
from dotenv import load_dotenv
from rich.console import Console
from rich.logging import RichHandler

load_dotenv()


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
if os.environ.get("LOG_CONSOLE", "0").lower() in ("1", "true"):
    handlers.append(rich_handler)
handlers.extend([
    logging.FileHandler("starbridge.log"),
    logfire.LogfireLoggingHandler(),
])

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=handlers,
)

log = logging.getLogger("starbridge")
