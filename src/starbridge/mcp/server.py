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
        self.notes: dict[str, str] = {}
        self.server = Server("starbridge")
        self._confluence_handler = starbridge.confluence.Handler()
        self._register_handlers()

    def _register_handlers(self):
        @self.server.list_resources()
        async def handle_list_resources() -> list[types.Resource]:
            resources = []
            resources += self._confluence_handler.resource_list()
            return resources

        @self.server.read_resource()
        async def handle_read_resource(uri: AnyUrl) -> str:
            if (uri.scheme, uri.host) == ("starbridge", "confluence"):
                return self._confluence_handler.resource_get(uri)

            raise ValueError(
                f"Unsupported URI scheme/host combination: {uri.scheme}:{uri.host}"
            )

        @self.server.list_prompts()
        async def handle_list_prompts() -> list[types.Prompt]:
            prompts = []
            prompts += self._confluence_handler.prompt_list()
            return prompts

        @self.server.get_prompt()
        async def handle_get_prompt(
            name: str, arguments: dict[str, str] | None
        ) -> types.GetPromptResult:
            if name.startswith("starbridge-confluence-"):
                method = getattr(
                    self._confluence_handler,
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
        async def handle_list_tools() -> list[types.Tool]:
            tools = []
            tools += starbridge.confluence.Handler.get_tools()
            return tools

        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: dict | None
        ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
            if name.startswith("starbridge-confluence-"):
                method = getattr(
                    self._confluence_handler,
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


async def run_server():
    server = MCPServer()
    await server.run()
