"""Web module for interacting with the world wide web."""

from .cli import cli
from .models import Context, GetResult, LinkTarget, Resource, RobotForbiddenError
from .service import Service
from .settings import Settings

__all__ = [
    "Context",
    "GetResult",
    "LinkTarget",
    "Resource",
    "RobotForbiddenError",
    "Service",
    "Settings",
    "cli",
]
