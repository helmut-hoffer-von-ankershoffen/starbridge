"""
MCP Service module providing base classes and utilities for Model Context Protocol services.

This module contains the core service abstractions including resource handling,
tool management, and prompt processing for MCP-compatible services.
"""

from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from inspect import signature
from typing import TypeVar
from urllib.parse import urlparse

from mcp import types
from pydantic_settings import BaseSettings

from starbridge.mcp.context import MCPContext
from starbridge.mcp.models import ResourceMetadata
from starbridge.utils import Health, description_and_params, load_settings

T = TypeVar("T", bound=BaseSettings)


@dataclass(frozen=True)
class ResourceType:
    """A resource type is identified by a triple of (server, service, type)."""

    server: str
    service: str
    type: str

    def __str__(self) -> str:
        """
        Return string representation as 'server://service/type'.

        Returns:
            str: Resource type in format 'server://service/type'

        """
        return f"{self.server}://{self.service}/{self.type}"


class MCPBaseService(ABC):
    """Base class for MCP services."""

    _settings: BaseSettings

    def __init__(self, settings_class: type[T] | None = None) -> None:
        """
        Initialize service with optional settings.

        Args:
            settings_class: Optional settings class to load configuration.

        """
        if settings_class is not None:
            self._settings = self._load_settings(settings_class)

    @abstractmethod
    def info(self) -> dict:
        """Get info about configuration of this service. Override in subclass."""

    @abstractmethod
    def health(self, context: MCPContext | None = None) -> Health:
        """Get health of this service. Override in subclass."""

    def tool_list(self, context: MCPContext | None = None) -> list[types.Tool]:  # noqa: ARG002
        """
        Get available tools.

        Args:
            context (MCPContext | None): MCP context for the operation

        Returns:
            list[types.Tool]: List of available tools discovered via @mcp_tool decorator.

        """
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
                    ),
                )
        return tools

    def resource_list(self, context: MCPContext | None = None) -> list[types.Resource]:
        """
        Get available resources by discovering and calling all resource iterators.

        Args:
            context (MCPContext | None): MCP context for the operation

        Returns:
            list[types.Resource]: List of available resources.

        Raises:
            ValueError: If duplicate resource types are found.

        """
        resources = []
        type_map = defaultdict(list)

        for method_name in dir(self.__class__):
            method = getattr(self.__class__, method_name)
            if hasattr(method, "__mcp_resource_iterator__"):
                meta = method.__mcp_resource_iterator__
                if not meta.type:
                    msg = f"Resource iterator {method_name} missing required type"
                    raise ValueError(
                        msg,
                    )

                self._check_type_uniqueness(type_map, meta, method_name)
                iterator_resources = method(self, context)

                for resource in iterator_resources:
                    self._validate_resource_uri(resource, meta)
                resources.extend(iterator_resources)

        return resources

    def resource_type_list(
        self,
        context: MCPContext | None = None,  # noqa: ARG002
    ) -> set[ResourceMetadata]:
        """
        Get available resource types by discovering all resource iterators.

        Args:
            context (MCPContext | None): MCP context for the operation

        Returns:
            set[ResourceMetadata]: Set of available resource metadata types.

        """
        types = set()
        for method_name in dir(self.__class__):
            method = getattr(self.__class__, method_name)
            if hasattr(method, "__mcp_resource_iterator__"):
                meta = method.__mcp_resource_iterator__
                if meta.type:
                    types.add(meta)
        return types

    # Remove resource_get method as it's now handled by MCPServer

    def prompt_list(self, context: MCPContext | None = None) -> list[types.Prompt]:  # noqa: ARG002
        """
        Get available prompts by discovering decorated prompt methods.

        Args:
            context (MCPContext | None): MCP context for the operation

        Returns:
            list[types.Prompt]: List of available prompts.

        """
        prompts = []
        for method_name in dir(self.__class__):
            method = getattr(self.__class__, method_name)
            if hasattr(method, "__mcp_prompt__"):
                meta = method.__mcp_prompt__
                sig = signature(method)
                description, required, params = description_and_params(method)

                # Convert signature params to PromptArguments
                arguments = []
                for name in sig.parameters:
                    if name in {"self", "context"}:
                        continue
                    arguments.append(
                        types.PromptArgument(
                            name=name,
                            description=params.get(name, {}).get(
                                "description",
                                f"Parameter {name}",
                            ),
                            required=name in required,
                        ),
                    )

                prompts.append(
                    types.Prompt(
                        name=str(meta),
                        description=description,
                        arguments=arguments,
                    ),
                )
        return prompts

    @staticmethod
    def _validate_resource_uri(resource: types.Resource, meta: ResourceMetadata) -> None:
        """
        Validate resource URI against metadata.

        Raises:
            ValueError: If URI scheme, service or path does not match metadata.

        """
        parsed = urlparse(str(resource.uri))
        if parsed.scheme != meta.server:
            msg = f"Resource URI scheme '{parsed.scheme}' doesn't match decorator scheme '{meta.server}'"
            raise ValueError(
                msg,
            )
        if parsed.netloc != meta.service:
            msg = f"Resource URI service '{parsed.netloc}' doesn't match decorator service '{meta.service}'"
            raise ValueError(
                msg,
            )
        if not parsed.path.startswith(f"/{meta.type}/"):
            msg = f"Resource URI path doesn't start with '/{meta.type}/'"
            raise ValueError(msg)

    @staticmethod
    def _check_type_uniqueness(type_map: defaultdict[str, list[str]], meta: ResourceMetadata, method_name: str) -> None:
        """
        Ensure resource type is unique.

        Raises:
            ValueError: If multiple resource iterators are found for the same type.

        """
        type_map[meta.type].append(method_name)
        if len(type_map[meta.type]) > 1:
            msg = f"Multiple resource iterators found for type '{meta.type}': {type_map[meta.type]}"
            raise ValueError(
                msg,
            )

    @staticmethod
    def _load_settings(settings_class: type[T]) -> T:
        """
        Load settings from context.

        Returns:
            T: Loaded settings instance

        """
        return load_settings(settings_class)
