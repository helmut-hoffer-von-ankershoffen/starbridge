"""Search package for Starbridge providing search functionality and related services."""

from .cli import cli
from .service import Service
from .settings import Settings

__all__ = [
    "Service",
    "Settings",
    "cli",
]
