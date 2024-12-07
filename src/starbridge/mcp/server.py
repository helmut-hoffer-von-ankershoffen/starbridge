import importlib.metadata

import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from pydantic import AnyUrl

import starbridge.confluence

__version__ = importlib.metadata.version("starbridge")


class MCPServer:
    def __init__(self):
        self.server = Server("starbridge")
        self._confluence = starbridge.confluence.Service()
        self._register_handlers()

    def _register_handlers(self):
        @self.server.list_resources()
        async def resource_list() -> list[types.Resource]:
            resources = []
            resources += self._confluence.resource_list()
            return resources

        @self.server.read_resource()
        async def resource_get(uri: AnyUrl) -> str:
            if (uri.scheme, uri.host) == ("starbridge", "confluence"):
                return self._confluence.resource_get(uri)

            raise ValueError(
                f"Unsupported URI scheme/host combination: {uri.scheme}:{uri.host}"
            )

        @self.server.list_prompts()
        async def prompt_list() -> list[types.Prompt]:
            prompts = []
            prompts += starbridge.confluence.Service.prompt_list()
            return prompts

        @self.server.get_prompt()
        async def prompt_get(
            name: str, arguments: dict[str, str] | None
        ) -> types.GetPromptResult:
            if name.startswith("starbridge-confluence-"):
                method = getattr(
                    self._confluence,
                    f"mcp_prompt_{name.replace('-', '_')}",
                )
                if arguments:
                    return method(**arguments)
                return method()
            return types.GetPromptResult(
                description=None,
                messages=[],
            )

        @self.server.list_tools()
        async def tool_list() -> list[types.Tool]:
            tools = []
            tools += starbridge.confluence.Service.tool_list()
            return tools

        @self.server.call_tool()
        async def tool_call(
            name: str, arguments: dict | None
        ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
            if name.startswith("starbridge-confluence-"):
                method = getattr(
                    self._confluence,
                    f"mcp_tool_{name.replace('-', '_')}",
                )
                if arguments:
                    return method(**arguments)
                return method()

            raise ValueError(f"Unknown tool: {name}")

    async def run(self):
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="starbridge",
                    server_version=__version__,
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )


async def mcp_server():
    """Run MCP Server"""
    server = MCPServer()
    await server.run()
