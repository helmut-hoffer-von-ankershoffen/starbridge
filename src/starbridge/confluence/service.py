"""Handles Confluence operations."""

import json
import os

import mcp.types as types
import typer
from atlassian import Confluence
from pydantic import AnyUrl

from starbridge.mcp import MCPBaseService, MCPContext, mcp_tool
from starbridge.utils import get_logger

from . import cli

logger = get_logger(__name__)


class Service(MCPBaseService):
    """Service class for Confluence operations."""

    def __init__(self):
        self._url = os.environ.get("STARBRIDGE_ATLASSIAN_URL")
        self._email_address = os.environ.get("STARBRIDGE_ATLASSIAN_EMAIL_ADDRESS")
        self._api_token = os.environ.get("STARBRIDGE_ATLASSIAN_API_TOKEN")
        self._api = Confluence(
            url=self._url,
            username=self._email_address,
            password=self._api_token,
            cloud=True,
        )

    @classmethod
    def get_cli(cls) -> tuple[str | None, typer.Typer | None]:
        """Get CLI for Confluence service."""
        return "confluence", cli.cli

    def info(self) -> dict:
        logger.info("Confluence service info")
        return {
            "url": self._url,
            "email": self._email_address,
            "api_token": self._api_token,
        }

    @mcp_tool()
    def starbridge_confluence_info(self, context: MCPContext | None = None):
        """Info about Confluence environment"""
        return self.info()

    def health(self) -> str:
        try:
            spaces = self.space_list()
        except Exception as e:
            return f"DOWN: {str(e)}"
        if (
            isinstance(spaces, dict)
            and "results" in spaces
            and isinstance(spaces["results"], list)
        ):
            if len(spaces["results"]) > 0:
                return "UP"
        return "DOWN: No spaces found"

    def resource_list(self, context: MCPContext | None = None):
        spaces = self.space_list()
        return [
            types.Resource(
                uri=AnyUrl(f"starbridge://confluence/space/{space['key']}"),
                name=space["name"],
                description=f"Space of type '{space['type']}'",
                mimeType="application/json",
            )
            for space in spaces["results"]
        ]

    def resource_get(
        self,
        uri: AnyUrl,
        context: MCPContext | None = None,
    ) -> str:
        if (uri.scheme, uri.host) != ("starbridge", "confluence"):
            raise ValueError(
                f"Unsupported URI scheme/host combination: {uri.scheme}:{uri.host}"
            )
        if (uri.path or "").startswith("/space/"):
            space_key = uri.path.split("/")[-1]
            return json.dumps(self.space_info(space_key), indent=2)

    @staticmethod
    def prompt_list(context: MCPContext | None = None):
        return [
            types.Prompt(
                name="starbridge_confluence_space_summary",
                description="Creates a summary of spaces in Confluence",
                arguments=[
                    types.PromptArgument(
                        name="style",
                        description="Style of the summary (brief/detailed)",
                        required=False,
                    )
                ],
            )
        ]

    def mcp_prompt_starbridge_confluence_space_summary(
        self,
        style: str = "brief",
        context: MCPContext | None = None,
    ) -> types.GetPromptResult:
        detail_prompt = " Give extensive details." if style == "detailed" else ""
        return types.GetPromptResult(
            description="Summarize the current spaces",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Here are the current spaces to summarize:{detail_prompt}\n\n"
                        + "\n".join(
                            f"- {space['key']}: {space['name']} ({space['type']})"
                            for space in self.space_list()["results"]
                        ),
                    ),
                )
            ],
        )

    def space_info(self, space_key: str):
        return self._api.get_space(space_key)

    def space_list(self):
        return self._api.get_all_spaces()

    @mcp_tool()
    def starbridge_confluence_space_list(self, context: MCPContext | None = None):
        """List spaces in Confluence"""
        return self.space_list()

    def page_create(
        self,
        space_key: str,
        title: str,
        body: str,
        parent_id: str = None,
        representation: str = "wiki",
        editor: str = "v2",
        full_width: bool = True,
        status: str = "current",
    ):
        return self._api.create_page(
            space=space_key,
            title=title,
            body=body,
            parent_id=parent_id,
            type="page",
            representation=representation,
            editor=editor,
            full_width=full_width,
            status=status,
        )

    @mcp_tool()
    def starbridge_confluence_page_create(
        self,
        space_key: str,
        title: str,
        body: str,
        parent_id: str = None,
        draft: bool = False,
        context: MCPContext | None = None,
    ) -> str:
        """Create page in Confluence space given key of space, title and body of page and optional parent page id.

        Args:
            space_key (str): The key identifier of the Confluence space where the page will be created
            title (str): The title of the new page to be created
            body (str): The content/body of the new page
            parent_id (str, optional): The ID of the parent page if this is to be created as a child page. Defaults to None.
            draft (bool, optional): If to create the page in draft mode. Defaults to False, i.e. page will be published.

        Returns:
            The JSON response of the page creation
        """
        return (
            self.page_create(
                space_key=space_key,
                title=title,
                body=body,
                parent_id=parent_id,
                representation="wiki",
                editor="v2",
                full_width=True,
                status="draft" if draft else "current",
            ),
        )
