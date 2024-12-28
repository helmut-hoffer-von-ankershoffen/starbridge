from typing import Annotated

from pydantic import AnyHttpUrl, EmailStr, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from starbridge import __project_name__


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix=f"{__project_name__.upper()}_ATLASSIAN_",
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    url: Annotated[
        AnyHttpUrl,
        Field(
            description="Base url of your Confluence and Jira installation",
            examples=["https://example.atlassian.net"],
        ),
    ]

    email_address: Annotated[
        EmailStr,
        Field(
            description="Email address of your Atlassian account",
            examples=["you@your-domain.com"],
        ),
    ]

    api_token: Annotated[
        SecretStr,
        Field(
            description="API token of your Atlassian account. Go to https://id.atlassian.com/manage-profile/security/api-tokens to create a token.",
            examples=["YOUR_TOKEN"],
        ),
    ]
