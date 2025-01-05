"""Context handling for MCP operations and requests."""

from typing import Any, Literal

from mcp.shared.context import RequestContext, SessionT
from pydantic import AnyUrl, BaseModel


class MCPContext(BaseModel):  # pragma: no cover
    """Context object providing access to MCP capabilities."""

    _request_context: RequestContext | None
    _mcp: Any  # Avoid circular import by using Any

    def __init__(
        self,
        *,
        request_context: RequestContext | None = None,
        mcp: "mcp.server.MCPServer | None" = None,  # type: ignore
        **kwargs: dict[str, type[Any]],
    ) -> None:
        """
        Initialize MCP context.

        Args:
            request_context (RequestContext): Current request context if any
            mcp (MCPServer | None): Reference to MCP server instance
            **kwargs (dict[str, type[Any]]): Additional context parameters

        """
        super().__init__(**kwargs)
        self._request_context = request_context
        self._mcp = mcp

    @property
    def mcp(self) -> type[Any]:
        """Access to the MCP server."""
        return self._mcp

    @property
    def request_context(self) -> RequestContext:
        """
        Access the underlying request context.

        Returns:
            RequestContext: The current request context.

        Raises:
            RuntimeError: If context is accessed outside of a request.

        """
        if self._request_context is None:
            msg = "Context is not available outside of a request"
            raise RuntimeError(msg)
        return self._request_context

    async def report_progress(
        self,
        progress: float,
        total: float | None = None,
    ) -> None:
        """
        Report progress for the current operation.

        Args:
            progress: Current progress value e.g. 24
            total: Optional total value e.g. 100

        """
        progress_token = self.request_context.meta.progressToken if self.request_context.meta else None

        if not progress_token:
            return

        await self.request_context.session.send_progress_notification(
            progress_token=progress_token,
            progress=progress,
            total=total,
        )

    async def read_resource(self, uri: str | AnyUrl) -> str | bytes:
        """
        Read a resource by URI.

        Args:
            uri: Resource URI to read

        Returns:
            (str | AnyUrl): The resource content as either text or bytes

        """
        return await self._mcp.read_resource(uri)

    async def log(
        self,
        level: Literal["debug", "info", "warning", "error"],
        message: str,
        logger_name: str | None = None,
        **kwargs,  # noqa: ARG002
    ) -> None:
        """
        Send a log message to the client.

        Args:
            level (Literal["debug", "info", "warning", "error"]): Log level (debug, info, warning, error)
            message (str): Log message
            logger_name (str | None): Optional logger name
            **kwargs (dict[str, type[Any]]): Additional structured data to include

        """
        # TODO(@helmut-hoffer-von-ankershoffen): Inject kwargs into log message
        await self.request_context.session.send_log_message(
            level=level,
            data=message,
            logger=logger_name,
        )

    @property
    def client_id(self) -> str | None:
        """Get the client ID if available."""
        return getattr(self.request_context.meta, "client_id", None) if self.request_context.meta else None

    @property
    def request_id(self) -> str:
        """Get the unique ID for this request."""
        return str(self.request_context.request_id)

    @property
    def session(self) -> SessionT:  # type: ignore
        """
        Access to the underlying session for advanced usage.

        Returns:
            Session: The underlying session object

        """
        return self.request_context.session

    # Convenience methods for common log levels
    async def debug(self, message: str, logger_name: str | None = None, **kwargs) -> None:
        """
        Send a debug log message.

        Args:
            message (str): The message to log
            logger_name (str|Name): Name of the logger
            **kwargs (dict[str, type[Any]]): Additional structured data to include

        """
        await self.log("debug", message=message, logger_name=logger_name, **kwargs)

    async def info(self, message: str, logger_name: str | None = None, **kwargs) -> None:
        """
        Send an info log message.

        Args:
            message (str): The message to log
            logger_name (str|Name): Name of the logger
            **kwargs: Additional structured data to include

        """
        await self.log("info", message=message, logger_name=logger_name, **kwargs)

    async def warning(self, message: str, logger_name: str | None = None, **kwargs) -> None:
        """
        Send a warning log message.

        Args:
            message (str): The message to log
            logger_name (str|Name): Name of the logger
            **kwargs (dict[str, type[Any]]): Additional structured data to include

        """
        await self.log("warning", message=message, logger_name=logger_name, **kwargs)

    async def error(self, message: str, logger_name: str | None = None, **kwargs) -> None:
        """
        Send an error log message.

        Args:
            message (str): The message to log
            logger_name (str|Name): Name of the logger
            **kwargs (dict[str, type[Any]]): Additional structured data to include

        """
        await self.log("error", message=message, logger_name=logger_name, **kwargs)
