from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from inspect import signature
from typing import TypeVar
from urllib.parse import urlparse

import mcp.types as types
from pydantic_settings import BaseSettings

from starbridge.mcp.context import MCPContext
from starbridge.mcp.models import ResourceMetadata
from starbridge.utils import Health, description_and_params, load_settings

T = TypeVar("T", bound=BaseSettings)


@dataclass(frozen=True)
class ResourceType:
    """A resource type is identified by a triple of (server, service, type)"""

    server: str
    service: str
    type: str

    def __str__(self) -> str:
        return f"{self.server}://{self.service}/{self.type}"


class MCPBaseService(ABC):
    """Base class for MCP services."""

    _settings: BaseSettings

    def __init__(self, settings_class: type[T] | None = None):
        if settings_class is not None:
            self._settings = self._load_settings(settings_class)

    @abstractmethod
    def info(self) -> dict:
        """Get info about configuration of this service. Override in subclass."""

    @abstractmethod
    def health(self, context: MCPContext | None = None) -> Health:
        """Get health of this service. Override in subclass."""

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
        type_map = defaultdict(list)

        for method_name in dir(self.__class__):
            method = getattr(self.__class__, method_name)
            if hasattr(method, "__mcp_resource_iterator__"):
                meta = method.__mcp_resource_iterator__
                if not meta.type:
                    raise ValueError(
                        f"Resource iterator {method_name} missing required type"
                    )

                self._check_type_uniqueness(type_map, meta, method_name)
                iterator_resources = method(self, context)

                for resource in iterator_resources:
                    self._validate_resource_uri(resource, meta)
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

    def _validate_resource_uri(self, resource, meta):
        """Validate resource URI against metadata."""
        parsed = urlparse(str(resource.uri))
        if parsed.scheme != meta.server:
            raise ValueError(
                f"Resource URI scheme '{parsed.scheme}' doesn't match decorator scheme '{meta.server}'"
            )
        if parsed.netloc != meta.service:
            raise ValueError(
                f"Resource URI service '{parsed.netloc}' doesn't match decorator service '{meta.service}'"
            )
        if not parsed.path.startswith(f"/{meta.type}/"):
            raise ValueError(f"Resource URI path doesn't start with '/{meta.type}/'")

    def _check_type_uniqueness(self, type_map, meta, method_name):
        """Ensure resource type is unique."""
        type_map[meta.type].append(method_name)
        if len(type_map[meta.type]) > 1:
            raise ValueError(
                f"Multiple resource iterators found for type '{meta.type}': {type_map[meta.type]}"
            )

    def _load_settings(self, settings_class: type[T]) -> T:
        """Load settings from context."""
        return load_settings(settings_class)
