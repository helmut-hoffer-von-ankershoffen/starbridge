"""
MCP decorators module providing function decorators for registering MCP capabilities.

This module contains decorators for registering tools, resources, and prompts in the
Starbridge server.
"""

from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

from starbridge import __project_name__

from .models import PromptMetadata, ResourceMetadata, ToolMetadata

P = ParamSpec("P")
R = TypeVar("R")

"""Decorators for registering MCP capabilities like tools, resources and prompts."""


def mcp_tool(
    server: str = __project_name__,
    service: str | None = None,
    name: str | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Mark a method as an MCP tool.

    Args:
        server (str): The server name. Defaults to "starbridge".
        service (str): The service name. If not provided, derived from module name.
        name (str | None): The tool name. If not provided, derived from function name.

    Returns:
        Callable: Decorated function that registers as MCP tool.

    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> R:
            return func(*args, **kwargs)

        wrapper.__mcp_tool__ = ToolMetadata(  # type: ignore
            server=server,
            service=service or _get_service_name(func),
            name=name or func.__name__,
        )
        return wrapper

    return decorator


def mcp_resource_iterator(
    server: str = __project_name__,
    service: str | None = None,
    type: str | None = None,  # noqa: A002
) -> Callable:
    """
    Mark a method as a resource iterator.

    Args:
        server (str): The server name. Defaults to project name.
        service (str | None): The service name. Defaults to module name if not provided.
        type (str | None): The resource type.

    Returns:
        Callable: Decorated function that registers as a resource iterator.

    Raises:
        ValueError: If resource type is missing or duplicated.

    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> R:  # type: ignore
            return func(*args, **kwargs)

        wrapper.__mcp_resource_iterator__ = ResourceMetadata(  # type: ignore
            server=server,
            service=service or _get_service_name(func),
            type=type or "",
        )
        return wrapper

    return decorator


def mcp_resource(
    server: str = __project_name__,
    service: str | None = None,
    type: str | None = None,  # noqa: A002
) -> Callable:
    """
    Mark a method as a resource handler.

    Args:
        server (str): The server name. Defaults to project name.
        service (str | None): The service name. Defaults to module name if not provided.
        type (str | None): The resource type.

    Returns:
        Callable: Decorated function that registers as a resource handler.

    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> R:  # type: ignore
            return func(*args, **kwargs)

        wrapper.__mcp_resource__ = ResourceMetadata(  # type: ignore
            server=server,
            service=service or _get_service_name(func),
            type=type or "",
        )
        return wrapper

    return decorator


def mcp_prompt(
    server: str = __project_name__,
    service: str | None = None,
    type: str | None = None,  # noqa: A002
) -> Callable:
    """
    Mark a method as a prompt handler.

    Args:
        server (str): The server name. Defaults to project name.
        service (str | None): The service name. Defaults to module name if not provided.
        type (str | None): The prompt type. Defaults to method name without `prompt_` prefix.

    Returns:
        Callable: Decorated function that registers as a prompt handler.

    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> R:  # type: ignore
            return func(*args, **kwargs)

        wrapper.__mcp_prompt__ = PromptMetadata(  # type: ignore
            server=server,
            service=service or _get_service_name(func),
            type=type or func.__name__.replace("prompt_", ""),
        )
        return wrapper

    return decorator


def _get_service_name(func: Callable) -> str:
    """
    Extract service name from function's module path.

    Args:
        func (Callable): The function to extract module name from

    Returns:
        str: The extracted service name

    """
    return func.__module__.split(".")[1]
