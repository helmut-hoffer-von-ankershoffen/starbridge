from typing import Any, Literal

from mcp.shared.context import RequestContext
from pydantic import AnyUrl, BaseModel


class MCPContext(BaseModel):
    """Context object providing access to MCP capabilities."""

    _request_context: RequestContext | None
    _mcp: Any  # Avoid circular import by using Any

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
        return self._mcp

    @property
    def request_context(self) -> RequestContext:
        """Access to the underlying request context."""
        if self._request_context is None:
            raise RuntimeError("Context is not available outside of a request")
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
            (str | bytes): The resource content as either text or bytes
        """
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
            \*\*extra: Additional structured data to include
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
    async def debug(self, message: str, **extra: Any) -> None:
        """Send a debug log message."""
        await self.log("debug", message, **extra)

    async def info(self, message: str, **extra: Any) -> None:
        """Send an info log message."""
        await self.log("info", message, **extra)

    async def warning(self, message: str, **extra: Any) -> None:
        """Send a warning log message."""
        await self.log("warning", message, **extra)

    async def error(self, message: str, **extra: Any) -> None:
        """Send an error log message."""
        await self.log("error", message, **extra)
