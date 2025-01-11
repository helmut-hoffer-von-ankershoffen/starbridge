"""Logfire integration for instrumentation."""

from typing import Annotated

import logfire
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from starbridge import __project_name__, __version__
from starbridge.instrumentation.otel_mcp_instrumentation import MCPInstrumentor
from starbridge.utils.settings import load_settings


class LogfireSettings(BaseSettings):
    """Configuration settings for Logfire integration."""

    model_config = SettingsConfigDict(
        env_prefix=f"{__project_name__.upper()}_LOGFIRE_",
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    token: Annotated[
        SecretStr | None,
        Field(description="Logfire token", examples=["YOUR_TOKEN"], default=None),
    ]
    environment: Annotated[
        str,
        Field(
            description="Environment name",
            examples=["development", "production"],
            default="production",
        ),
    ]
    instrument_mcp: Annotated[
        bool,
        Field(description="Enable MCP instrumentation", default=True),
    ]
    instrument_system_metrics: Annotated[
        bool,
        Field(description="Enable system metrics instrumentation", default=False),
    ]


def logfire_initialize() -> bool | None:
    """
    Initialize Logfire integration.

    Returns:
        bool | None: True if initialized successfully, False or None otherwise

    """
    settings = load_settings(LogfireSettings)

    if settings.token is None:
        return False

    logfire.configure(
        send_to_logfire="if-token-present",
        token=settings.token.get_secret_value(),
        environment=settings.environment,
        service_name=__project_name__,
        console=False,
        code_source=logfire.CodeSource(
            repository="https://github.com/helmut-hoffer-von-ankershoffen/starbridge",
            revision=__version__,
            root_path="",
        ),
    )
    if settings.instrument_mcp:
        MCPInstrumentor().instrument()

    if settings.instrument_system_metrics:
        logfire.instrument_system_metrics(base="full")

    return None
