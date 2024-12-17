import importlib.metadata

import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from pydantic import AnyUrl

from starbridge.mcp.context import MCPContext
from starbridge.mcp.service import MCPBaseService

__version__ = importlib.metadata.version("starbridge")


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
                method = getattr(service, f"mcp_prompt_{name.replace('-', '_')}")
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
                        notification_options=NotificationOptions(
                            prompts_changed=False,
                            resources_changed=False,
                            tools_changed=False,
                        ),
                        experimental_capabilities={},
                    ),
                ),
            )


async def mcp_run_coroutine():
    """Run MCP Server"""
    server = MCPServer()
    await server.run()
