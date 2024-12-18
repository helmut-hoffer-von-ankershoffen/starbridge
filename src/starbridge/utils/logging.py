import importlib.metadata
import logging
import os

import click
import logfire
from dotenv import load_dotenv
from rich.console import Console
from rich.logging import RichHandler

__version__ = importlib.metadata.version("starbridge")
load_dotenv()

logfire.configure(
    send_to_logfire="if-token-present",
    service_name="starbridge",
    console=False,
    code_source=logfire.CodeSource(
        repository="https://github.com/helmut-hoffer-von-ankershoffen/starbridge",
        revision=__version__,
        root_path="",  # FIXME: root_path
    ),
)
logfire.instrument_system_metrics(base="full")
logfire.install_auto_tracing(modules=["starbridge.confluence"], min_duration=0.001)


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


def get_logger(name: str | None) -> logging.Logger:
    if (name is None) or (name == "starbridge"):
        return logging.getLogger("starbridge")
    return logging.getLogger(f"starbridge.{name}")
