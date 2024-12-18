from collections import defaultdict
from dataclasses import dataclass
from importlib.metadata import entry_points
from inspect import signature
from typing import Any
from urllib.parse import urlparse

import mcp.types as types
import typer

from starbridge.mcp.context import MCPContext
from starbridge.mcp.models import ResourceMetadata
from starbridge.utils.signature import description_and_params


@dataclass(frozen=True)
class ResourceType:
    """A resource type is identified by a triple of (server, service, type)"""

    server: str
    service: str
    type: str

    def __str__(self) -> str:
        return f"{self.server}://{self.service}/{self.type}"


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

    @staticmethod
    def get_services() -> list[type["MCPBaseService"]]:
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

    @staticmethod
    def get_cli() -> tuple[str | None, typer.Typer | None]:
        """Get CLI name and typer for this service if available.
        Returns a tuple of (name, typer) or (None, None) if no CLI available."""
        return None, None

    def info(self) -> dict:
        """Get info about configuration of this service. Override in subclass."""
        raise NotImplementedError

    def health(self, context: MCPContext | None = None) -> str:
        """Get health of this service. Override in subclass."""
        raise NotImplementedError

    def tool_list(self, context: MCPContext | None = None) -> list[types.Tool]:
        """Get available tools. Discovers tools by looking for methods decorated with @mcp_tool."""
        tools = []
        for method_name in dir(self.__class__):
            method = getattr(self.__class__, method_name)
            if hasattr(method, "__mcp_tool__"):
                meta = method.__mcp_tool__
                description, required, params = description_and_params(method)
                tools.append(
                    types.Tool(
                        name=str(meta),  # Use metadata string representation
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
        """Get available resources by discovering and calling all resource iterators."""
        resources = []
        type_map = defaultdict(list)  # renamed from prefix_map

        # Find all resource iterators
        for method_name in dir(self.__class__):
            method = getattr(self.__class__, method_name)
            if hasattr(method, "__mcp_resource_iterator__"):
                meta = method.__mcp_resource_iterator__
                if not meta.type:  # renamed from prefix
                    raise ValueError(
                        f"Resource iterator {method_name} missing required type"
                    )

                # Check type uniqueness
                type_map[meta.type].append(method_name)
                if len(type_map[meta.type]) > 1:
                    raise ValueError(
                        f"Multiple resource iterators found for type '{meta.type}': {type_map[meta.type]}"
                    )

                # Get resources from iterator
                iterator_resources = method(self, context)

                # Validate each resource URI
                for resource in iterator_resources:
                    parsed = urlparse(str(resource.uri))
                    if parsed.scheme != meta.server:
                        raise ValueError(
                            f"Resource URI scheme '{parsed.scheme}' doesn't match decorator scheme '{meta.server}'"
                        )
                    if parsed.netloc != meta.service:
                        raise ValueError(
                            f"Resource URI service '{parsed.netloc}' doesn't match decorator service '{meta.service}'"
                        )
                    if not parsed.path.startswith(
                        f"/{meta.type}/"
                    ):  # renamed from prefix
                        raise ValueError(
                            f"Resource URI path doesn't start with '/{meta.type}/'"
                        )

                resources.extend(iterator_resources)

        return resources

    def resource_type_list(
        self, context: MCPContext | None = None
    ) -> set[ResourceMetadata]:
        """Get available resource types by discovering all resource iterators."""
        types = set()
        for method_name in dir(self.__class__):
            method = getattr(self.__class__, method_name)
            if hasattr(method, "__mcp_resource_iterator__"):
                meta = method.__mcp_resource_iterator__
                if meta.type:
                    types.add(meta)
        return types

    # Remove resource_get method as it's now handled by MCPServer

    def prompt_list(self, context: MCPContext | None = None) -> list[types.Prompt]:
        """Get available prompts by discovering decorated prompt methods."""
        prompts = []
        for method_name in dir(self.__class__):
            method = getattr(self.__class__, method_name)
            if hasattr(method, "__mcp_prompt__"):
                meta = method.__mcp_prompt__
                sig = signature(method)
                description, required, params = description_and_params(method)

                # Convert signature params to PromptArguments
                arguments = []
                for name, _param in sig.parameters.items():
                    if name in ("self", "context"):
                        continue
                    arguments.append(
                        types.PromptArgument(
                            name=name,
                            description=params.get(name, {}).get(
                                "description", f"Parameter {name}"
                            ),
                            required=name in required,
                        )
                    )

                prompts.append(
                    types.Prompt(
                        name=str(meta),
                        description=description,
                        arguments=arguments,
                    )
                )
        return prompts

    def get_prompt(
        self,
        name: str,
        arguments: dict[str, Any] | None,
        context: MCPContext | None = None,
    ) -> types.GetPromptResult:
        """Get prompt content. Override in subclass."""
        return types.GetPromptResult(description=None, messages=[])
