from dataclasses import dataclass


@dataclass(frozen=True)
class ResourceMetadata:
    """A resource type is identified by a triple of (server, service, type)."""

    server: str
    service: str
    type: str

    def __str__(self) -> str:
        return f"{self.server}://{self.service}/{self.type}"


@dataclass(frozen=True)
class PromptMetadata:
    """A prompt is identified by server, service, and type."""

    server: str
    service: str
    type: str

    def __str__(self) -> str:
        return f"{self.server}_{self.service}_{self.type}"


@dataclass(frozen=True)
class ToolMetadata:
    """A tool is identified by server, service, and name."""

    server: str
    service: str
    name: str

    def __str__(self) -> str:
        return f"{self.server}_{self.service}_{self.name}"
