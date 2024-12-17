from importlib.metadata import entry_points
from typing import Any

import mcp.types as types
import typer
from pydantic import AnyUrl

from starbridge.mcp.context import MCPContext
from starbridge.utils.signature import description_and_params


class MCPBaseService:
    """Base class for MCP services."""

    @property
    def service_prefix(self) -> str:
        """
        Automatically generate service prefix from the module path.
        Example: 'starbridge.confluence.service.Service' becomes 'starbridge-confluence-'
        """
        # Get full module path of the actual service class
        module_path = self.__class__.__module__
        # Take the first three parts (e.g., 'starbridge.confluence.service')
        # and convert dots to dashes
        prefix = "_".join(module_path.split(".")[:2]) + "_"
        return prefix

    @classmethod
    def get_services(cls) -> list[type["MCPBaseService"]]:
        """Discover all registered MCP services."""
        services = []
        for entry_point in entry_points(group="starbridge.services"):
            try:
                service_class = entry_point.load()
                if issubclass(service_class, MCPBaseService):
                    services.append(service_class)
            except Exception as e:
                print(f"Error loading service {entry_point.name}: {e}")
        return services

    @classmethod
    def get_cli(cls) -> tuple[str | None, typer.Typer | None]:
        """Get CLI name and typer for this service if available.
        Returns a tuple of (name, typer) or (None, None) if no CLI available."""
        return None, None

    def info(self) -> dict:
        """Get info about configuration of this service. Override in subclass."""
        raise NotImplementedError

    def health(self) -> str:
        """Get health of this service. Override in subclass."""
        raise NotImplementedError

    def tool_list(self, context: MCPContext | None = None) -> list[types.Tool]:
        """Get available tools. Discovers tools by looking for methods decorated with @mcp_tool."""
        tools = []
        for method_name in dir(self.__class__):
            method = getattr(self.__class__, method_name)
            if hasattr(method, "__mcp_tool__"):
                description, required, params = description_and_params(method)
                tools.append(
                    types.Tool(
                        name=method.__mcp_tool__,
                        description=description,
                        inputSchema={
                            "type": "object",
                            "required": required,
                            "properties": params,
                        },
                    )
                )
        return tools

    def resource_list(self, context: MCPContext | None = None) -> list[types.Resource]:
        """Get available resources. Override in subclass."""
        return []

    def resource_get(self, context: MCPContext, uri: AnyUrl) -> str | None:
        """Get resource content. Override in subclass."""
        return None

    def prompt_list(self, context: MCPContext | None = None) -> list[types.Prompt]:
        """Get available prompts. Override in subclass."""
        return []

    def get_prompt(
        self, name: str, arguments: dict[str, Any] | None, context: MCPContext
    ) -> types.GetPromptResult:
        """Get prompt content. Override in subclass."""
        return types.GetPromptResult(description=None, messages=[])
