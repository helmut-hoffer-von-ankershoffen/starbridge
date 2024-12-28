from typing import Annotated

import logfire
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from starbridge import __project_name__, __version__
from starbridge.instrumentation.otel_mcp_instrumentation import MCPInstrumentor
from starbridge.utils.settings import load_settings


class LogfireSettings(BaseSettings):
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
    instrument_mcp_enabled: Annotated[
        bool, Field(description="Enable MCP instrumentation", default=False)
    ]


def logfire_initialize():
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
    logfire.instrument_system_metrics(base="full")

    if settings.instrument_mcp_enabled:
        MCPInstrumentor().instrument()
