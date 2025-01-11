"""Settings used for interacting with the world wide web."""

from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from starbridge import __project_name__, __version__


class Settings(BaseSettings):
    """Settings for web module."""

    model_config = SettingsConfigDict(
        env_prefix=f"{__project_name__.upper()}_WEB_",
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    user_agent: Annotated[
        str,
        Field(
            default=f"starbridge/{__version__} (Autonomous; https://github.com/helmut-hoffer-von-ankershoffen/starbridge)",
            description="User agent to use when fetching URLs.",
        ),
    ]

    respect_robots_txt: Annotated[
        bool,
        Field(
            default=True,
            description="Whether to respect robots.txt files when interacting with the web as an agent.",
        ),
    ]

    timeout: Annotated[int, Field(default=60, description="Timeout for web requests.")]
