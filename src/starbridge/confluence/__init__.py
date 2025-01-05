"""Confluence API integration module for interacting with Confluence pages and spaces."""

from .cli import cli
from .service import Service

__all__ = ["Service", "cli"]
