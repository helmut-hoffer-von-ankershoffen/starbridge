import importlib.metadata
from typing import Any, Literal

import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.shared.context import RequestContext
from pydantic import AnyUrl, BaseModel

import starbridge.confluence

__version__ = importlib.metadata.version("starbridge")


class MCPServer:
    """MCP Server for Starbridge."""

    def __init__(self):
        self._confluence = starbridge.confluence.Service()

        self._server = Server("starbridge")
        self._server.list_prompts()(self.prompt_list)
        self._server.get_prompt()(self.prompt_get)
        self._server.list_resources()(self.resource_list)
        self._server.read_resource()(self.resource_get)
        self._server.list_tools()(self.tool_list)
        self._server.call_tool()(self.tool_call)

    def get_context(self) -> "MCPContext":
        """
        Returns a Context object. Note that the context will only be valid
        during a request; outside a request, most methods will error.
        """
        try:
            request_context = self._server.request_context
        except LookupError:
            request_context = None
        return MCPContext(request_context=request_context, mcp=self)

    async def resource_list(self) -> list[types.Resource]:
        resources = []
        resources += self._confluence.resource_list(context=self.get_context())
        return resources

    async def resource_get(self, uri: AnyUrl) -> str:
        if (uri.scheme, uri.host) == ("starbridge", "confluence"):
            return self._confluence.resource_get(uri=uri, context=self.get_context())

        raise ValueError(
            f"Unsupported URI scheme/host combination: {uri.scheme}:{uri.host}"
        )

    async def prompt_list(
        self,
    ) -> list[types.Prompt]:
        prompts = []
        prompts += starbridge.confluence.Service.prompt_list(context=self.get_context())
        return prompts

    async def prompt_get(
        self, name: str, arguments: dict[str, str] | None
    ) -> types.GetPromptResult:
        if name.startswith("starbridge-confluence-"):
            method = getattr(
                self._confluence,
                f"mcp_prompt_{name.replace('-', '_')}",
            )
            if arguments:
                arguments = arguments.copy()
                arguments.pop("context", None)
                return method(**arguments, context=self.get_context())
            return method(context=self.get_context())
        return types.GetPromptResult(
            description=None,
            messages=[],
        )

    async def tool_list(
        self,
    ) -> list[types.Tool]:
        tools = []
        tools += starbridge.confluence.Service.tool_list(context=self.get_context())
        return tools

    async def tool_call(
        self, name: str, arguments: dict | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        if name.startswith("starbridge-confluence-"):
            method = getattr(
                self._confluence,
                f"mcp_tool_{name.replace('-', '_')}",
            )
            if arguments:
                arguments = arguments.copy()
                arguments.pop("context", None)
                return method(**arguments, context=self.get_context())
            return method(context=self.get_context())

        raise ValueError(f"Unknown tool: {name}")

    async def run(self):
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self._server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="starbridge",
                    server_version=__version__,
                    capabilities=self._server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )


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
    _mcp: MCPServer | None

    def __init__(
        self,
        *,
        request_context: RequestContext | None = None,
        mcp: MCPServer | None = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self._request_context = request_context
        self._mcp = mcp

    @property
    def mcp(self) -> MCPServer:
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


async def mcp_run_coroutine():
    """Run MCP Server"""
    server = MCPServer()
    await server.run()
