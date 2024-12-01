import json

import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from pydantic import AnyUrl


class StarbridgeServer:
    def __init__(self):
        self.notes: dict[str, str] = {}
        self.server = Server("starbridge")
        self._register_handlers()

    def _register_handlers(self):
        @self.server.list_resources()
        async def handle_list_resources() -> list[types.Resource]:
            return [
                types.Resource(
                    uri=AnyUrl(f"note://internal/{name}"),
                    name=f"Note: {name}",
                    description=f"A simple note named {name}",
                    mimeType="text/plain",
                )
                for name in self.notes
            ]

        @self.server.read_resource()
        async def handle_read_resource(uri: AnyUrl) -> str:
            if uri.scheme != "note":
                raise ValueError(f"Unsupported URI scheme: {uri.scheme}")

            name = uri.path
            if name is not None:
                name = name.lstrip("/")
                return self.notes[name]
            raise ValueError(f"Note not found: {name}")

        @self.server.list_prompts()
        async def handle_list_prompts() -> list[types.Prompt]:
            return [
                types.Prompt(
                    name="summarize-notes",
                    description="Creates a summary of all notes",
                    arguments=[
                        types.PromptArgument(
                            name="style",
                            description="Style of the summary (brief/detailed)",
                            required=False,
                        )
                    ],
                )
            ]

        @self.server.get_prompt()
        async def handle_get_prompt(
            name: str, arguments: dict[str, str] | None
        ) -> types.GetPromptResult:
            if name != "summarize-notes":
                raise ValueError(f"Unknown prompt: {name}")

            style = (arguments or {}).get("style", "brief")
            detail_prompt = " Give extensive details." if style == "detailed" else ""

            return types.GetPromptResult(
                description="Summarize the current notes",
                messages=[
                    types.PromptMessage(
                        role="user",
                        content=types.TextContent(
                            type="text",
                            text=f"Here are the current notes to summarize:{detail_prompt}\n\n"
                            + "\n".join(
                                f"- {name}: {content}"
                                for name, content in self.notes.items()
                            ),
                        ),
                    )
                ],
            )

        @self.server.list_tools()
        async def handle_list_tools() -> list[types.Tool]:
            return [
                types.Tool(
                    name="add-note",
                    description="Add a new note",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "content": {"type": "string"},
                        },
                        "required": ["name", "content"],
                    },
                ),
                types.Tool(
                    name="get-notes",
                    description="Get all notes",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                    },
                ),
            ]

        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: dict | None
        ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
            match name:
                case "add-note":
                    if not arguments:
                        raise ValueError("Missing arguments")
                    return await self.add_note(arguments)
                case "get-notes":
                    return await self.get_notes()
                case _:
                    raise ValueError(f"Unknown tool: {name}")

    async def add_note(
        self, arguments: dict
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        note_name = arguments.get("name")
        content = arguments.get("content")

        if not note_name or not content:
            raise ValueError("Missing name or content")

        self.notes[note_name] = content
        try:
            await self.server.request_context.session.send_resource_list_changed()
        except LookupError:
            pass

        return [
            types.TextContent(
                type="text",
                text=f"Added note '{note_name}' with content: {content}",
            )
        ]

    async def get_notes(
        self,
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        return [types.TextContent(type="text", text=json.dumps(self.notes, indent=2))]

    async def run(self):
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="starbridge",
                    server_version="0.1.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )


async def run_server():
    server = StarbridgeServer()
    await server.run()
