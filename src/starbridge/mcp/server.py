"""
MCP Server implementation for Starbridge.

This module provides the main server implementation for Model Context Protocol,
including HTTP and stdio transport handling, service registration, and request routing.
"""

import asyncio
import base64
import json
import os
import signal
from io import BytesIO
from typing import Any
from urllib.parse import ParseResult, urlparse

import mcp.server.stdio
import pydantic_core
from mcp import types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.sse import SseServerTransport
from mcp.types import (
    EmbeddedResource,
    ImageContent,
    TextContent,
)
from starlette.requests import Request as StarletteRequest

try:
    from PIL import Image

    _has_imaging = True
except ImportError:
    _has_imaging = False

from pydantic import AnyUrl
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route

from starbridge import __project_name__, __version__
from starbridge.mcp.context import MCPContext
from starbridge.mcp.decorators import mcp_tool
from starbridge.mcp.models import ResourceMetadata
from starbridge.mcp.service import MCPBaseService
from starbridge.utils import AggregatedHealth, get_logger, locate_subclasses

logger = get_logger(__name__)


class MCPServer:  # noqa: PLR0904
    """MCP Server for Starbridge."""

    def __init__(self) -> None:
        """Dynamically locate and register services."""
        self._services = []
        for service_class in MCPServer.service_classes():
            self._services.append(service_class())

        self._server = Server(__project_name__)
        self._server.list_prompts()(self.prompt_list)
        self._server.get_prompt()(self.prompt_get)
        self._server.list_resources()(self.resource_list)
        self._server.read_resource()(self.resource_get)
        self._server.list_tools()(self.tool_list)
        self._server.call_tool()(self.tool_call)

    @mcp_tool()
    def health(self, context: MCPContext | None = None) -> AggregatedHealth:  # noqa: ARG002
        """
        Get health status of all services and their dependencies.

        Returns:
            AggregatedHealth: Combined health status of all services.

        """
        dependencies = {}
        for service in self._services:
            service_name = service.__class__.__module__.split(".")[1]
            dependencies[service_name] = service.health()

        return AggregatedHealth(dependencies=dependencies)

    def get_context(self) -> MCPContext:
        """
        Get a context object for the current request.

        Returns:
            MCPContext: Context object for current request.

        Note:
            Context will only be valid during a request.
            Outside a request, most methods will error.

        """
        try:
            request_context = self._server.request_context
        except LookupError:
            request_context = None
        return MCPContext(request_context=request_context, mcp=self)

    async def resource_list(self) -> list[types.Resource]:
        """
        List all available resources across services.

        Returns:
            list[types.Resource]: List of available resources.

        """
        resources = []
        for service in self._services:
            result = service.resource_list(context=self.get_context())
            if asyncio.iscoroutine(result):
                result = await result
            resources.extend(result)
        return resources

    def _find_resource_handler(self, parsed_uri: ParseResult) -> tuple[MCPBaseService | None, Any]:
        """
        Find the appropriate resource handler for a parsed URI.

        Args:
            parsed_uri (ParseResult): Parsed URL to find handler for.

        Returns:
            tuple: Service instance and handler method.

        """
        for service in self._services:
            for method_name in dir(service.__class__):
                method = getattr(service.__class__, method_name)
                if not hasattr(method, "__mcp_resource__"):
                    continue

                meta = method.__mcp_resource__
                if (
                    meta.server == parsed_uri.scheme
                    and meta.service == parsed_uri.netloc
                    and parsed_uri.path.startswith(f"/{meta.type}/")
                ):
                    return service, method
        return None, None

    async def resource_get(self, uri: AnyUrl) -> str:
        """
        Get a resource from any service that can handle it.

        Args:
            uri (AnyUrl): URI of the resource to get.

        Returns:
            str: The resource content.

        Raises:
            ValueError: If no service is found to handle the URI.

        """
        parsed = urlparse(str(uri))
        service, handler = self._find_resource_handler(parsed)

        if handler:
            result = handler(
                service,
                parsed.path.split("/")[-1],
                context=self.get_context(),
            )
            if asyncio.iscoroutine(result):
                result = await result
            if result is not None:
                return result

        msg = f"No service found for URI: {uri}"
        raise ValueError(msg)

    async def prompt_list(self) -> list[types.Prompt]:
        """
        Get all available prompts across services.

        Returns:
            list[types.Prompt]: List of available prompts.

        """
        prompts = []
        for service in self._services:
            result = service.prompt_list(context=self.get_context())
            if asyncio.iscoroutine(result):
                result = await result
            prompts.extend(result)
        return prompts

    def _find_prompt_handler(self, name: str) -> tuple[MCPBaseService | None, Any]:
        """
        Find the appropriate prompt handler for a given name.

        Args:
            name: Full name of the prompt to find.

        Returns:
            tuple[MCPBaseService | None, Any]: Service instance and handler method, or None if not found.

        """
        server, service, prompt_type = name.split("_", 2)

        for service_instance in self._services:
            for method_name in dir(service_instance.__class__):
                method = getattr(service_instance.__class__, method_name)
                if not hasattr(method, "__mcp_prompt__"):
                    continue

                meta = method.__mcp_prompt__
                if meta.server == server and meta.service == service and meta.type == prompt_type:
                    return service_instance, method
        return None, None

    async def prompt_get(
        self,
        name: str,
        arguments: dict[str, str] | None,
    ) -> types.GetPromptResult:
        """
        Get a prompt by its full name (server_service_type).

        Args:
            name: Full prompt name in format server_service_type
            arguments: Optional arguments to pass to the prompt

        Returns:
            types.GetPromptResult: The prompt result containing description and messages

        """
        service_instance, method = self._find_prompt_handler(name)

        if method:
            if arguments:
                arguments = arguments.copy()
                arguments.pop("context", None)
                result = method(
                    service_instance,
                    **arguments,
                    context=self.get_context(),
                )
            else:
                result = method(service_instance, context=self.get_context())
            if asyncio.iscoroutine(result):
                result = await result
            return result

        return types.GetPromptResult(description=None, messages=[])

    async def tool_list(self) -> list[types.Tool]:
        """
        Get all available tools across services.

        Returns:
            list[types.Tool]: List of available tools.

        """
        tools = []
        for service in self._services:
            result = service.tool_list(context=self.get_context())
            if asyncio.iscoroutine(result):
                result = await result
            tools.extend(result)
        return tools

    def _find_tool_handler(self, name: str) -> tuple[MCPBaseService | None, Any]:
        """
        Find the appropriate tool handler for a given name.

        Args:
            name: Name of the tool to find

        Returns:
            tuple[MCPBaseService | None, Any]: Service instance and handler method, or None if not found

        """
        server, service, tool_name = name.split("_", 2)

        for service_instance in self._services:
            for method_name in dir(service_instance.__class__):
                method = getattr(service_instance.__class__, method_name)
                if not hasattr(method, "__mcp_tool__"):
                    continue

                meta = method.__mcp_tool__
                if meta.server == server and meta.service == service and meta.name == tool_name:
                    return service_instance, method
        return None, None

    async def tool_call(
        self,
        name: str,
        arguments: dict | None,
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """
        Execute an MCP tool by name.

        Args:
            name: Name of the tool to call
            arguments: Optional arguments to pass to the tool

        Returns:
            list[types.TextContent | types.ImageContent | types.EmbeddedResource]: Tool execution results

        Raises:
            ValueError: If tool is not found

        """
        service_instance, method = self._find_tool_handler(name)

        if method:
            if arguments:
                arguments = arguments.copy()
                arguments.pop("context", None)
                result = method(
                    service_instance,
                    **arguments,
                    context=self.get_context(),
                )
            else:
                result = method(service_instance, context=self.get_context())
            if asyncio.iscoroutine(result):
                result = await result
            return MCPServer._marshal_result(result)

        msg = f"Unknown tool: {name}"
        raise ValueError(msg)

    async def resource_type_list(self) -> set[ResourceMetadata]:
        """
        Get all available resource types across all services.

        Returns:
            set[ResourceMetadata]: Set of resource metadata from all services.

        """
        types = set()
        for service in self._services:
            result = service.resource_type_list(context=self.get_context())
            if asyncio.iscoroutine(result):
                result = await result
            types.update(result)
        return types

    @staticmethod
    def resource_types() -> list[str]:
        """
        Get all available resource types as formatted strings.

        Returns:
            list[str]: Sorted list of resource types as formatted strings.

        """
        return sorted(str(rt) for rt in asyncio.run(MCPServer().resource_type_list()))

    def starlette_app(self, debug: bool = True) -> Starlette:
        """
        Create Starlette ASGI application for serving MCP over HTTP.

        Args:
            debug: Enable debug mode

        Returns:
            Starlette: Configured ASGI application

        """
        sse = SseServerTransport("/messages")

        async def handle_sse(request: StarletteRequest) -> None:
            async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,  # noqa: SLF001
            ) as streams:
                await self._server.run(
                    streams[0],
                    streams[1],
                    self._create_initialization_options(),
                )

        async def handle_messages(request: StarletteRequest) -> None:
            await sse.handle_post_message(request.scope, request.receive, request._send)  # noqa: SLF001

        def handle_health(request: StarletteRequest) -> PlainTextResponse:  # noqa: ARG001
            return PlainTextResponse(
                headers={"content-type": "application/json"},
                content=json.dumps(
                    self.health().model_dump(),
                ),  # Use json.dumps instead of model_dump_json
            )

        def handle_terminate(request: StarletteRequest) -> None:  # noqa: ARG001
            os.kill(os.getpid(), signal.SIGINT)
            os.kill(os.getpid(), signal.SIGINT)

        return Starlette(
            debug=debug,
            routes=[
                Route("/health", endpoint=handle_health, methods=["GET"]),
                Route("/terminate", endpoint=handle_terminate, methods=["GET"]),
                Route("/sse", endpoint=handle_sse),
                Route("/messages", endpoint=handle_messages, methods=["POST"]),
            ],
        )

    async def run_stdio(self) -> None:
        """Run MCP server over stdin/stdout."""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self._server.run(
                read_stream,
                write_stream,
                self._create_initialization_options(),
            )

    @staticmethod
    def service_classes() -> list[type["MCPBaseService"]]:
        """
        Get all available MCP service classes.

        Returns:
            list[type[MCPBaseService]]: List of service class types

        """
        return locate_subclasses(MCPBaseService)  # type: ignore

    @staticmethod
    def tools() -> list[types.Tool]:
        """
        Get all available MCP tools.

        Returns:
            list[types.Tool]: List of available tools

        """
        return asyncio.run(MCPServer().tool_list())

    @staticmethod
    def tool(
        name: str,
        arguments: dict | None = None,
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """
        Call an MCP tool by name.

        Args:
            name: Name of the tool to call
            arguments: Optional arguments to pass to the tool

        Returns:
            list[types.TextContent | types.ImageContent | types.EmbeddedResource]: Tool execution results

        """
        return asyncio.run(MCPServer().tool_call(name, arguments))

    @staticmethod
    def resources() -> list[types.Resource]:
        """
        Get all available MCP resources.

        Returns:
            list[types.Resource]: List of available resources

        """
        return asyncio.run(MCPServer().resource_list())

    @staticmethod
    def resource(uri: str) -> str:
        """
        Get a resource by URI.

        Args:
            uri: URI of the resource to get

        Returns:
            str: Resource content

        """
        return asyncio.run(MCPServer().resource_get(AnyUrl(uri)))

    @staticmethod
    def prompts() -> list[types.Prompt]:
        """
        Get all available prompts.

        Returns:
            list[types.Prompt]: List of available prompts

        """
        return asyncio.run(MCPServer().prompt_list())

    @staticmethod
    def prompt(name: str, arguments: dict | None = None) -> types.GetPromptResult:
        """
        Get a prompt by name.

        Args:
            name: Name of the prompt to get
            arguments: Optional arguments to pass to the prompt

        Returns:
            types.GetPromptResult: Prompt result

        """
        return asyncio.run(MCPServer().prompt_get(name, arguments))

    @staticmethod
    def serve(host: str | None = None, port: int | None = None, debug: bool = True) -> None:
        """
        Start the MCP server.

        Args:
            host: Host to bind to (for HTTP server)
            port: Port to bind to (for HTTP server)
            debug: Enable debug mode

        Returns:
            None

        """
        if host and port:
            import uvicorn  # noqa: PLC0415 (performance)

            uvicorn.run(
                MCPServer().starlette_app(debug),
                host=host,
                port=port,
                log_level=str.lower(os.environ.get("LOGLEVEL", "INFO")),
                log_config=None,
            )
        else:
            return asyncio.run(MCPServer().run_stdio())
        return None

    def _create_initialization_options(self) -> InitializationOptions:
        return InitializationOptions(
            server_name=__project_name__,
            server_version=__version__,
            capabilities=self._server.get_capabilities(
                notification_options=NotificationOptions(
                    prompts_changed=False,
                    resources_changed=False,
                    tools_changed=False,
                ),
                experimental_capabilities={},
            ),
        )

    @staticmethod
    def _marshal_result(  # noqa: PLR0911
        result: type[Any],
    ) -> list[TextContent | ImageContent | EmbeddedResource]:
        """
        Marshals a result into a sequence of TextContent, ImageContent, or EmbeddedResource.

        Returns:
            list[TextContent | ImageContent | EmbeddedResource]: The marshalled result sequence.

        """
        if result is None:
            return []

        if isinstance(result, TextContent | ImageContent | EmbeddedResource):
            return [result]

        if isinstance(result, str):
            return [TextContent(type="text", text=result)]

        if _has_imaging and isinstance(result, Image.Image):
            mime_type = (
                Image.MIME.get(result.format, "application/octet-stream")
                if result.format
                else "application/octet-stream"
            )
            data = BytesIO()
            result.save(data, format=result.format)
            return [
                ImageContent(
                    type="image",
                    data=base64.b64encode(data.getvalue()).decode("utf-8"),
                    mimeType=mime_type,
                ),
            ]

        if isinstance(result, list | tuple):
            return [item for subresult in result for item in MCPServer._marshal_result(subresult)]

        try:
            return [
                TextContent(
                    type="text",
                    text=json.dumps(pydantic_core.to_jsonable_python(result), indent=2),
                ),
            ]
        except Exception:
            logger.exception("Error converting result to JSON")

        return [TextContent(type="text", text=str(result))]
