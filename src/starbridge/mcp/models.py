"""Data models for MCP functionality."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ResourceMetadata:
    """
    A resource type is identified by a triple of (server, service, type).

    Args:
        server (str): The server name.
        service (str): The service name.
        type (str): The resource type.

    """

    server: str
    service: str
    type: str

    def __str__(self) -> str:
        """
        Convert resource metadata to string representation.

        Returns:
            str: String representation in format "server://service/type"

        """
        return f"{self.server}://{self.service}/{self.type}"


@dataclass(frozen=True)
class PromptMetadata:
    """
    A prompt is identified by server, service, and type.

    Args:
        server (str): The server name.
        service (str): The service name.
        type (str): The prompt type.

    """

    server: str
    service: str
    type: str

    def __str__(self) -> str:
        """
        Convert prompt metadata to string representation.

        Returns:
            str: String representation in format "server_service_type"

        """
        return f"{self.server}_{self.service}_{self.type}"


@dataclass(frozen=True)
class ToolMetadata:
    """
    A tool is identified by server, service, and name.

    Args:
        server (str): The server name.
        service (str): The service name.
        name (str): The tool name.

    """

    server: str
    service: str
    name: str

    def __str__(self) -> str:
        """
        Convert tool metadata to string representation.

        Returns:
            str: String representation in format "server_service_name"

        """
        return f"{self.server}_{self.service}_{self.name}"
