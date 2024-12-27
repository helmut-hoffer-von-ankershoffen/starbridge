from pydantic import AnyUrl, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AtlassianSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="STARBRIDGE_ATLASSIAN_",
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    url: AnyUrl = Field(
        description="Base url of your Confluence and Jira installation",
        examples=["https://example.atlassian.net"],
    )
    email_address: str = Field(
        description="Email address of your Atlassian account",
        examples=["you@your-domain.com"],
    )
    api_token: SecretStr = Field(
        description="API token of your Atlassian account. Go to https://id.atlassian.com/manage-profile/security/api-tokens to create a token.",
        examples=["YOUR_TOKEN"],
    )
