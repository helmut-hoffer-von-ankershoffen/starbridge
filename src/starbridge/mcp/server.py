import asyncio
import base64
import json
import os
import signal
from io import BytesIO
from typing import Any
from urllib.parse import urlparse

import mcp.server.stdio
import mcp.types as types
import pydantic_core
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.sse import SseServerTransport
from mcp.types import (
    EmbeddedResource,
    ImageContent,
    TextContent,
)

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


class MCPServer:
    """MCP Server for Starbridge."""

    def __init__(self):
        # dynamically locate and register services
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
    def health(self, context: MCPContext | None = None) -> AggregatedHealth:
        """Health of services and their dependencies"""
        dependencies = {}
        for service in self._services:
            service_name = service.__class__.__module__.split(".")[1]
            dependencies[service_name] = service.health()

        return AggregatedHealth(dependencies=dependencies)

    def get_context(self) -> MCPContext:
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
        for service in self._services:
            resources.extend(service.resource_list(context=self.get_context()))
        return resources

    def _find_resource_handler(self, parsed_uri):
        """Find the appropriate resource handler for a parsed URI."""
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
        """Get a resource from any service that can handle it."""
        parsed = urlparse(str(uri))
        service, handler = self._find_resource_handler(parsed)

        if handler:
            result = handler(
                service,
                parsed.path.split("/")[-1],
                context=self.get_context(),
            )
            if result is not None:
                return result

        raise ValueError(f"No service found for URI: {uri}")

    async def prompt_list(
        self,
    ) -> list[types.Prompt]:
        prompts = []
        for service in self._services:
            prompts.extend(service.prompt_list(context=self.get_context()))
        return prompts

    def _find_prompt_handler(self, name: str):
        """Find the appropriate prompt handler for a given name."""
        server, service, prompt_type = name.split("_", 2)

        for service_instance in self._services:
            for method_name in dir(service_instance.__class__):
                method = getattr(service_instance.__class__, method_name)
                if not hasattr(method, "__mcp_prompt__"):
                    continue

                meta = method.__mcp_prompt__
                if (
                    meta.server == server
                    and meta.service == service
                    and meta.type == prompt_type
                ):
                    return service_instance, method
        return None, None

    async def prompt_get(
        self, name: str, arguments: dict[str, str] | None
    ) -> types.GetPromptResult:
        """Get a prompt by its full name (server_service_type)."""
        service_instance, method = self._find_prompt_handler(name)

        if method:
            if arguments:
                arguments = arguments.copy()
                arguments.pop("context", None)
                return method(service_instance, **arguments, context=self.get_context())
            return method(service_instance, context=self.get_context())

        return types.GetPromptResult(description=None, messages=[])

    async def tool_list(
        self,
    ) -> list[types.Tool]:
        tools = []
        for service in self._services:
            tools.extend(service.tool_list(context=self.get_context()))
        return tools

    def _find_tool_handler(self, name: str):
        """Find the appropriate tool handler for a given name."""
        server, service, tool_name = name.split("_", 2)

        for service_instance in self._services:
            for method_name in dir(service_instance.__class__):
                method = getattr(service_instance.__class__, method_name)
                if not hasattr(method, "__mcp_tool__"):
                    continue

                meta = method.__mcp_tool__
                if (
                    meta.server == server
                    and meta.service == service
                    and meta.name == tool_name
                ):
                    return service_instance, method
        return None, None

    async def tool_call(
        self, name: str, arguments: dict | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        service_instance, method = self._find_tool_handler(name)

        if method:
            if arguments:
                arguments = arguments.copy()
                arguments.pop("context", None)
                result = method(
                    service_instance, **arguments, context=self.get_context()
                )
            else:
                result = method(service_instance, context=self.get_context())
            if asyncio.iscoroutine(result):
                result = await result
            return MCPServer._marshal_result(result)

        raise ValueError(f"Unknown tool: {name}")

    async def resource_type_list(self) -> set[ResourceMetadata]:
        """Get all available resource types across all services."""
        types = set()
        for service in self._services:
            types.update(service.resource_type_list(context=self.get_context()))
        return types

    @staticmethod
    def resource_types() -> list[str]:
        """Get all available resource types as formatted strings."""
        return sorted(str(rt) for rt in asyncio.run(MCPServer().resource_type_list()))

    def starlette_app(self, debug: bool = True) -> Starlette:
        sse = SseServerTransport("/messages")

        async def handle_sse(request):
            async with sse.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await self._server.run(
                    streams[0], streams[1], self._create_initialization_options()
                )

        async def handle_messages(request):
            await sse.handle_post_message(request.scope, request.receive, request._send)

        async def handle_health(request):
            return PlainTextResponse(
                headers={"content-type": "application/json"},
                content=json.dumps(
                    self.health().model_dump()
                ),  # Use json.dumps instead of model_dump_json
            )

        async def handle_terminate(request):
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

    async def run_stdio(self):
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self._server.run(
                read_stream,
                write_stream,
                self._create_initialization_options(),
            )

    @staticmethod
    def service_classes() -> list[type["MCPBaseService"]]:
        return locate_subclasses(MCPBaseService)  # type: ignore

    @staticmethod
    def tools() -> list[types.Tool]:
        return asyncio.run(MCPServer().tool_list())

    @staticmethod
    def tool(
        name: str, arguments: dict | None = None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        return asyncio.run(MCPServer().tool_call(name, arguments))

    @staticmethod
    def resources() -> list[types.Resource]:
        return asyncio.run(MCPServer().resource_list())

    @staticmethod
    def resource(uri: str) -> str:
        return asyncio.run(MCPServer().resource_get(AnyUrl(uri)))

    @staticmethod
    def prompts() -> list[types.Prompt]:
        return asyncio.run(MCPServer().prompt_list())

    @staticmethod
    def prompt(name: str, arguments: dict | None = None) -> types.GetPromptResult:
        return asyncio.run(MCPServer().prompt_get(name, arguments))

    @staticmethod
    def serve(host: str | None = None, port: int | None = None, debug: bool = True):
        if host and port:
            import uvicorn

            uvicorn.run(
                MCPServer().starlette_app(debug),
                host=host,
                port=port,
                log_level=str.lower(os.environ.get("LOGLEVEL", "INFO")),
                log_config=None,
            )
        else:
            return asyncio.run(MCPServer().run_stdio())

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
    def _marshal_result(
        result: Any,
    ) -> list[TextContent | ImageContent | EmbeddedResource]:
        """Marshals a result into a sequence of TextContent, ImageContent, or EmbeddedResource."""
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
                )
            ]

        if isinstance(result, list | tuple):
            return [
                item
                for subresult in result
                for item in MCPServer._marshal_result(subresult)
            ]

        try:
            return [
                TextContent(
                    type="text",
                    text=json.dumps(pydantic_core.to_jsonable_python(result)),
                )
            ]
        except Exception as e:
            logger.error(f"Error converting result to JSON: {e}")

        return [TextContent(type="text", text=str(result))]
