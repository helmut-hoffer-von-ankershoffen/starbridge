from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def mcp_tool(name: str | None = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator to mark a method as an MCP tool.

    Args:
        name (str, optional): The tool name. If not provided, will convert the method name to kebab-case.
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        tool_name = name
        if tool_name is None:
            tool_name = func.__name__

        wrapper.__mcp_tool__ = tool_name
        return wrapper

    return decorator
