"""Settings used for searching."""

from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from starbridge import __project_name__


class Settings(BaseSettings):
    """Settings for search module."""

    model_config = SettingsConfigDict(
        env_prefix=f"{__project_name__.upper()}_SEARCH_",
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    brave_search_api_key: Annotated[
        str,
        Field(
            ...,
            description="Brave Search API Key (see https://brave.com/search/api/).",
        ),
    ]
