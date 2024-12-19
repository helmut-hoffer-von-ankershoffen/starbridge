from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class AtlassianSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="STARBRIDGE_ATLASSIAN_",
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    url: AnyUrl | None = None
    email_address: str | None = None
    api_token: str | None = None
