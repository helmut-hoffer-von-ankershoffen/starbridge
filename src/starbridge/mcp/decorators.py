from collections.abc import Callable
from functools import wraps


def mcp_tool(name: str | None = None):
    """Decorator to mark a method as an MCP tool.

    Args:
        name (str, optional): The tool name. If not provided, will convert the method name to kebab-case.
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Store the tool name on the function
        tool_name = name
        if tool_name is None:
            # Convert method name to kebab-case, removing any mcp_tool_ prefix
            method_name = func.__name__
            tool_name = method_name

        wrapper.__mcp_tool__ = tool_name
        return wrapper

    return decorator
