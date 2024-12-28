"""Handles Confluence operations."""

import json
import os

import mcp.types as types
from atlassian import Confluence
from pydantic import AnyUrl

from starbridge.atlassian.settings import Settings
from starbridge.mcp import (
    MCPBaseService,
    MCPContext,
    mcp_prompt,
    mcp_resource,
    mcp_resource_iterator,
    mcp_tool,
)
from starbridge.utils import Health, get_logger

logger = get_logger(__name__)


class Service(MCPBaseService):
    """Service class for Confluence operations."""

    _settings: Settings

    def __init__(self):
        super().__init__(Settings)
        self._api = Confluence(
            url=str(self._settings.url),
            username=self._settings.email_address,
            password=self._settings.api_token.get_secret_value(),
            cloud=True,
        )

    @mcp_tool()
    def health(self, context: MCPContext | None = None) -> Health:
        try:
            spaces = self.space_list()
        except Exception as e:
            return Health(status=Health.Status.DOWN, reason=str(e))
        if (
            isinstance(spaces, dict)
            and "results" in spaces
            and isinstance(spaces["results"], list)
            and len(spaces["results"]) > 0
        ):
            return Health(status=Health.Status.UP)
        return Health(status=Health.Status.DOWN, reason="No spaces found")

    @mcp_tool()
    def info(self, context: MCPContext | None = None):
        """Info about Confluence environment"""
        return {
            "url": self._settings.url,
            "email_address": self._settings.email_address,
            "api_token": f"MASKED ({len(self._settings.api_token)} characters)",
        }

    @mcp_resource_iterator(type="space")
    def space_iterator(self, context: MCPContext | None = None):
        """List available Confluence spaces."""
        spaces = self.space_list()
        return [
            types.Resource(
                uri=AnyUrl(f"starbridge://confluence/space/{space['key']}"),
                name=space["name"],
                description=f"Space of type '{space['type']}: {space['description']}",
                mimeType="application/json",
            )
            for space in spaces["results"]
        ]

    @mcp_resource(type="space")
    def space_get(self, space_key: str, context: MCPContext | None = None) -> str:
        """Get specific Confluence space by key."""
        # Mock response if requested
        if "atlassian.Confluence.get_space" in os.environ.get("MOCKS", "").split(","):
            with open("tests/fixtures/get_space.json") as f:
                return json.dumps(json.load(f), indent=2)
        return json.dumps(self._api.get_space(space_key), indent=2)

    @mcp_prompt(type="space_summary")
    def space_summary(
        self,
        style: str = "brief",
        context: MCPContext | None = None,
    ) -> types.GetPromptResult:
        """Creates a summary of spaces in Confluence.

        Args:
            style: Style of the summary {'brief', 'detailed'}, defaults to 'brief'
        """
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

    @mcp_tool()
    def space_list(
        self,
        start: int = 0,
        limit: int = 1000,
        expand: str = "metadata,icon,description,homepage",
        space_type=None,
        space_status="current",
        context: MCPContext | None = None,
    ) -> dict:
        """List spaces in Confluence.

        Args:
            start: The starting index of the returned spaces
            start: The starting index of the returned spaces (defaults to 0)
            limit: Maximum number of spaces to return (defaults to 1000)
            expand: A comma-separated list of properties to expand in the response (defaults to 'metadata,icon,description,homepage')
            space_type: Filter by space type (e.g., 'global', 'personal', defaults to None, i.e. returns all types)
            space_status: Filter by space status ('current' or 'archived', defaults to current)
            context: MCP context for the operation

        Returns:
            (dict): JSON response containing the spaces list under 'results' key
        """
        # Mock response if requested
        if "atlassian.Confluence.get_all_spaces" in os.environ.get("MOCKS", "").split(
            ","
        ):
            with open("tests/fixtures/get_all_spaces.json") as f:
                return json.load(f)
        return self._api.get_all_spaces(
            start,
            limit,
            expand,
            space_type,
            space_status,
        )  # type: ignore

    @mcp_tool()
    def page_create(
        self,
        space: str,
        title: str,
        body: str,
        type: str = "page",
        parent_id: str | None = None,
        representation: str = "storage",
        editor: str | None = None,
        full_width: bool = False,
        status: str = "current",
        context: MCPContext | None = None,
    ):  # -> Response | Any | None:# -> Response | Any | None:# -> Response | Any | None:  # -> Response | Any | bytes | Any | None | str:
        """Create page in Confluence space.

        Args:
            space: The identifier of the Confluence space
            title: The title of the new page
            body: The content/body of the new page
            type: The type of content to create (defaults to 'page')
            parent_id: The ID of the parent page if this is a child page (defaults to None)
            representation: The representation of the content ('storage' or 'wiki', defaults to 'storage')
            editor: The editor to use for the page (defaults to None, alternative is 'v2')
            full_width: If to use full width layout (defaults to False)
            status: The status of the page (defaults to None, i.e. 'current')
        """
        return self._api.create_page(
            space,
            title,
            body,
            parent_id,
            type,
            representation,
            editor,
            full_width,
            status,
        )

    @mcp_tool()
    def page_get(
        self,
        page_id: str,
        status: str | None = None,
        expand: str | None = None,
        version: str | None = None,
        context: MCPContext | None = None,
    ):  # -> Response | Any | bytes | Any | None | str:
        """Get a specific Confluence page by its ID.

        Args:
            page_id: The ID of the page to retrieve
            status: Page status to retrieve ('current' or specific version, defaults to None, i.e. current version)
            expand: A comma-separated list of properties to expand in the response (defaults to None, i.e. 'history,space,version')
            version: Specific version number to retrieve (optional)
            context: MCP context for the operation

        Returns:
            (Any): JSON response containing the page details
        """
        return self._api.get_page_by_id(page_id, status, expand, version)

    @mcp_tool()
    def page_update(
        self,
        page_id: str,
        title: str,
        body: str,
        parent_id: str | None = None,
        type: str = "page",
        representation: str = "storage",
        minor_edit: bool = False,
        version_comment: str | None = None,
        always_update: bool = False,
        full_width: bool = False,
    ):
        """Update a Confluence page.

        Args:
            page_id: The ID of the page to update
            title: The new title for the page
            body: The new content/body for the page
            parent_id: The ID of the parent page if moving the page
            type: The type of content to update (defaults to 'page')
            representation: The representation of the content ('storage' or 'wiki', defaults to 'storage')
            minor_edit: Whether this is a minor edit (defaults to False)
            version_comment: Optional comment to describe the change
            always_update: Force update even if version conflict (defaults to False)
            full_width: If to use full width layout (defaults to False)

        Returns:
            (Any): JSON response containing the updated page details

        Notes:
            The 'storage' representation is the default Confluence storage format.
            The 'wiki' representation allows using wiki markup syntax.
        """
        return self._api.update_page(
            page_id,
            title,
            body,
            parent_id,
            type,
            representation,
            minor_edit,
            version_comment,
            always_update,
            full_width,
        )

    @mcp_tool()
    def page_delete(
        self,
        page_id: str,
        status: str | None = None,
        recursive: bool = False,
        context: MCPContext | None = None,
    ):
        """Delete a Confluence page.

        Args:
            page_id: The ID of the page to delete
            status: OPTIONAL: type of page
            recursive: if True - will recursively delete all children pages too (defaults to False)
            context: MCP context for the operation
        """
        return self._api.remove_page(page_id, status, recursive)

    @mcp_tool()
    def page_list(
        self,
        space_key: str,
        start: int = 0,
        limit: int = 1000,
        status: str | None = None,
        expand: str | None = None,
        content_type: str = "page",
        context: MCPContext | None = None,
    ):  # -> Any | Any:# -> Any | Any:
        """List pages in a Confluence space.

        Args:
            space_key: The key of the space to get pages from
            start: The starting index of the returned pages (defaults to 0)
            limit: Maximum number of pages to return (defaults to 1000)
            status: Filter by page status ('current' or 'archived', defaults to None, i.e. all pages)
            expand: A comma-separated list of properties to expand in the response (defaults to None, i.e. 'history,space,version')
            content_type: The type of content to return (defaults to 'page')
            context: MCP context for the operation

        Returns:
            (Any): List of pages in the specified space
        """
        return self._api.get_all_pages_from_space(
            space_key,
            start,
            limit,
            status,
            expand,
            content_type,
        )
