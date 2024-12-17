from typing import Any, Literal

from mcp.shared.context import RequestContext
from pydantic import AnyUrl, BaseModel


class MCPContext(BaseModel):
    """Context object providing access to MCP capabilities.

    This provides a cleaner interface to MCP's RequestContext functionality.
    It gets injected into tool and resource functions that request it via type hints.

    To use context in a tool function, add a parameter with the Context type annotation:

    ```python
    @server.tool()
    def my_tool(
        x: int,
        ctx: Context,
    ) -> str:
        # Log messages to the client
        ctx.info(
            f"Processing {x}"
        )
        ctx.debug(
            "Debug info"
        )
        ctx.warning(
            "Warning message"
        )
        ctx.error(
            "Error message"
        )

        # Report progress
        ctx.report_progress(
            50, 100
        )

        # Access resources
        data = ctx.read_resource(
            "resource://data"
        )

        # Get request info
        request_id = ctx.request_id
        client_id = ctx.client_id

        return str(x)
    ```

    The context parameter name can be anything as long as it's annotated with Context.
    The context is optional - tools that don't need it can omit the parameter.
    """

    _request_context: RequestContext | None
    _mcp: Any | None  # Avoid circular import by using Any

    def __init__(
        self,
        *,
        request_context: RequestContext | None = None,
        mcp: Any | None = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self._request_context = request_context
        self._mcp = mcp

    @property
    def mcp(self) -> Any:
        """Access to the MCP server."""
        if self._mcp is None:
            raise ValueError("Context is not available outside of a request")
        return self._mcp

    @property
    def request_context(self) -> RequestContext:
        """Access to the underlying request context."""
        if self._request_context is None:
            raise ValueError("Context is not available outside of a request")
        return self._request_context

    async def report_progress(
        self, progress: float, total: float | None = None
    ) -> None:
        """Report progress for the current operation.

        Args:
            progress: Current progress value e.g. 24
            total: Optional total value e.g. 100
        """

        progress_token = (
            self.request_context.meta.progressToken
            if self.request_context.meta
            else None
        )

        if not progress_token:
            return

        await self.request_context.session.send_progress_notification(
            progress_token=progress_token, progress=progress, total=total
        )

    async def read_resource(self, uri: str | AnyUrl) -> str | bytes:
        """Read a resource by URI.

        Args:
            uri: Resource URI to read

        Returns:
            The resource content as either text or bytes
        """
        assert self._mcp is not None, "Context is not available outside of a request"
        return await self._mcp.read_resource(uri)

    async def log(
        self,
        level: Literal["debug", "info", "warning", "error"],
        message: str,
        *,
        logger_name: str | None = None,
    ) -> None:
        """Send a log message to the client.

        Args:
            level: Log level (debug, info, warning, error)
            message: Log message
            logger_name: Optional logger name
            **extra: Additional structured data to include
        """
        await self.request_context.session.send_log_message(
            level=level, data=message, logger=logger_name
        )

    @property
    def client_id(self) -> str | None:
        """Get the client ID if available."""
        return (
            getattr(self.request_context.meta, "client_id", None)
            if self.request_context.meta
            else None
        )

    @property
    def request_id(self) -> str:
        """Get the unique ID for this request."""
        return str(self.request_context.request_id)

    @property
    def session(self):
        """Access to the underlying session for advanced usage."""
        return self.request_context.session

    # Convenience methods for common log levels
    def debug(self, message: str, **extra: Any) -> None:
        """Send a debug log message."""
        self.log("debug", message, **extra)

    def info(self, message: str, **extra: Any) -> None:
        """Send an info log message."""
        self.log("info", message, **extra)

    def warning(self, message: str, **extra: Any) -> None:
        """Send a warning log message."""
        self.log("warning", message, **extra)

    def error(self, message: str, **extra: Any) -> None:
        """Send an error log message."""
        self.log("error", message, **extra)