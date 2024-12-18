import asyncio
import base64
import importlib.metadata
import json
import os
from collections.abc import Sequence
from typing import Any

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
from PIL import Image
from pydantic import AnyUrl
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route

from starbridge.mcp.context import MCPContext
from starbridge.mcp.service import MCPBaseService
from starbridge.utils import get_logger

__version__ = importlib.metadata.version("starbridge")
logger = get_logger(__name__)


class MCPServer:
    """MCP Server for Starbridge."""

    def __init__(self):
        self._services = []
        for service_class in MCPBaseService.get_services():
            self._services.append(service_class())

        self._server = Server("starbridge")
        self._server.list_prompts()(self.prompt_list)
        self._server.get_prompt()(self.prompt_get)
        self._server.list_resources()(self.resource_list)
        self._server.read_resource()(self.resource_get)
        self._server.list_tools()(self.tool_list)
        self._server.call_tool()(self.tool_call)

    @classmethod
    def get_health(cls):
        """Health of services and their dependencies"""
        dependencies = {}
        for service_class in MCPBaseService.get_services():
            service = service_class()
            service_name = service.__class__.__module__.split(".")[1]
            dependencies[service_name] = service.health()

        healthy = all(status == "UP" for status in dependencies.values())
        logger.info(
            'Health check: {"healthy": %s, "dependencies": %s}', healthy, dependencies
        )
        return {"healthy": healthy, "dependencies": dependencies}

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

    async def resource_get(self, uri: AnyUrl) -> str:
        for service in self._services:
            result = service.resource_get(uri=uri, context=self.get_context())
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

    async def prompt_get(
        self, name: str, arguments: dict[str, str] | None
    ) -> types.GetPromptResult:
        for service in self._services:
            if name.startswith(service.service_prefix):
                method = getattr(service, f"mcp_prompt_{name}")
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
        for service in self._services:
            tools.extend(service.tool_list(context=self.get_context()))
        return tools

    async def tool_call(
        self, name: str, arguments: dict | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        for service in self._services:
            if name.startswith(service.service_prefix):
                method = getattr(service, name)
                if arguments:
                    arguments = arguments.copy()
                    arguments.pop("context", None)
                    return MCPServer._marshal_result(
                        method(**arguments, context=self.get_context())
                    )
                return MCPServer._marshal_result(method(context=self.get_context()))

        raise ValueError(f"Unknown tool: {name}")

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
                content=json.dumps({"health": True}),
            )

        return Starlette(
            debug=debug,
            routes=[
                Route("/health", endpoint=handle_health, methods=["GET"]),
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

    @classmethod
    def tools(cls) -> list[types.Tool]:
        return asyncio.run(MCPServer().tool_list())

    @classmethod
    def resources(cls) -> list[types.Resource]:
        return asyncio.run(MCPServer().resource_list())

    @classmethod
    def prompts(cls) -> list[types.Prompt]:
        return asyncio.run(MCPServer().prompt_list())

    @classmethod
    def serve(
        cls, host: str | None = None, port: int | None = None, debug: bool = True
    ):
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
            asyncio.run(MCPServer().run_stdio())

    def _create_initialization_options(self) -> InitializationOptions:
        return InitializationOptions(
            server_name="starbridge",
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

    @classmethod
    def _marshal_result(
        cls,
        result: Any,
    ) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """Marshals a result into a sequence of TextContent, ImageContent, or EmbeddedResource."""
        if result is None:
            return []

        if isinstance(result, TextContent | ImageContent | EmbeddedResource):
            return [result]

        if isinstance(result, str):
            return [TextContent(type="text", text=result)]

        if isinstance(result, Image.Image):
            return [
                ImageContent(
                    type="image",
                    data=base64.b64encode(result.tobytes()).decode("utf-8"),
                    mimeType=result.get_format_mimetype(),
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
