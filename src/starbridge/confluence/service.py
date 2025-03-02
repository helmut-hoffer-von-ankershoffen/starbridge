"""Handles Confluence operations."""

import json
import os
from pathlib import Path
from typing import Any

from atlassian import Confluence
from mcp import types
from pydantic import AnyUrl
from requests import Response

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

    def __init__(self) -> None:
        """Initialize the Confluence service with settings."""
        super().__init__(Settings)
        self._api = Confluence(
            url=str(self._settings.url),
            username=self._settings.email_address,
            password=self._settings.api_token.get_secret_value(),
            cloud=True,
        )

    @mcp_tool()
    def health(self, context: MCPContext | None = None) -> Health:  # noqa: ARG002
        """
        Check health of the Confluence service.

        Args:
            context (MCPContext | None): MCP context for the operation

        Returns:
            Health: The health status of the service

        """
        try:
            spaces = self.space_list()
        except Exception as e:  # noqa: BLE001
            return Health(status=Health.Status.DOWN, reason=str(e))
        if (
            isinstance(spaces, dict)
            and "results" in spaces  # type: ignore
            and isinstance(spaces["results"], list)  # type: ignore
            and len(spaces["results"]) > 0  # type: ignore
        ):
            return Health(status=Health.Status.UP)
        return Health(status=Health.Status.DOWN, reason="No spaces found")

    @mcp_tool()
    def info(self, context: MCPContext | None = None) -> dict[str, str]:  # noqa: ARG002
        """
        Info about Confluence environment.

        Args:
            context (MCPContext | None): MCP context for the operation

        Returns:
            dict[str, str]: Dictionary containing Confluence connection information

        """
        return {
            "url": str(self._settings.url),
            "email_address": self._settings.email_address,
            "api_token": f"MASKED ({len(self._settings.api_token)} characters)",
        }

    @mcp_resource_iterator(type="space")
    def space_iterator(self, context: MCPContext | None = None) -> list[types.Resource]:  # noqa: ARG002
        """
        List available Confluence spaces.

        Args:
            context (MCPContext | None): MCP context for the operation

        Raises:
            HTTPError: If the request to the Confluence API fails

        Returns:
            list[types.Resource]: List of resources representing Confluence spaces.

        """
        spaces = self.space_list()
        return [
            types.Resource(
                uri=AnyUrl(f"starbridge://confluence/space/{space['key']}"),  # type: ignore
                name=space["name"],  # type: ignore
                description=f"Space of type '{space['type']}: {space['description']}",  # type: ignore
                mimeType="application/json",
            )
            for space in spaces["results"]  # type: ignore
        ]

    @mcp_resource(type="space")
    def space_get(self, space_key: str, context: MCPContext | None = None) -> str:  # noqa: ARG002
        """
        Get specific Confluence space by key.

        Args:
            space_key (str): Key of the space to get
            context (MCPContext | None): MCP context for the operation

        Raises:
            HTTPError: If the request to the Confluence API fails

        Returns:
            str: JSON string containing the space details

        """
        # Mock response if requested
        if "atlassian.Confluence.get_space" in os.environ.get("MOCKS", "").split(","):
            with Path("tests/fixtures/get_space.json").open(encoding="utf-8") as f:
                return json.dumps(json.load(f), indent=2)
        return json.dumps(self._api.get_space(space_key), indent=2)

    @mcp_prompt(type="space_summary")
    def space_summary(
        self,
        style: str = "brief",
        context: MCPContext | None = None,  # noqa: ARG002
    ) -> types.GetPromptResult:
        """
        Create a summary of spaces in Confluence.

        Args:
            style (str): Style of the summary {'brief', 'detailed'}, defaults to 'brief'
            context (MCPContext | None): MCP context for the operation

        Raises:
            HTTPError: If the request to the Confluence API fails

        Returns:
            types.GetPromptResult: Prompt result containing the space summary.

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
                            f"- {space['key']}: {space['name']} ({space['type']})"  # type: ignore
                            for space in self.space_list()["results"]  # type: ignore
                        ),
                    ),
                ),
            ],
        )

    @mcp_tool()
    def space_list(  # noqa: PLR0913, PLR0917
        self,
        start: int = 0,
        limit: int = 1000,
        expand: str = "metadata,icon,description,homepage",
        space_type: str | None = None,
        space_status: str = "current",
        context: MCPContext | None = None,  # noqa: ARG002
    ) -> Response | type[Any] | bytes | str | None:
        """
        List spaces in Confluence.

        Args:
            start(int): The starting index of the returned spaces (defaults to 0)
            limit (int): Maximum number of spaces to return (defaults to 1000)
            expand (str): A comma-separated list of properties to expand in the response
                (defaults to 'metadata,icon,description,homepage')
            space_type (str|None): Filter by space type (e.g., 'global', 'personal',
                defaults to None, i.e. returns all types)
            space_status (str): Filter by space status ('current' or 'archived', defaults to current)
            context (MCPContext): MCP context for the operation

        Raises:
            HTTPError: If the request to the Confluence API fails

        Returns:
            Response | type[Any] | bytes | str | None: JSON response containing the spaces list under 'results' key

        """
        # Mock response if requested
        if "atlassian.Confluence.get_all_spaces" in os.environ.get("MOCKS", "").split(","):
            with Path("tests/fixtures/get_all_spaces.json").open(encoding="utf-8") as f:
                return json.load(f)
        return self._api.get_all_spaces(
            start,
            limit,
            expand,
            space_type,
            space_status,
        )

    @mcp_tool()
    def page_create(  # noqa: PLR0913, PLR0917
        self,
        space: str,
        title: str,
        body: str,
        type: str = "page",  # noqa: A002
        parent_id: str | None = None,
        representation: str = "storage",
        editor: str | None = None,
        full_width: bool = False,
        status: str = "current",
        context: MCPContext | None = None,  # noqa: ARG002
    ) -> Response | type[Any] | bytes | str | None:
        """
        Create page in Confluence space.

        Args:
            space (str): The identifier of the Confluence space
            title (str): The title of the new page
            body (str): The content/body of the new page
            type (str): The type of content to create (defaults to 'page')
            parent_id (str | None): The ID of the parent page if this is a child page (defaults to None)
            representation (str): The representation of the content ('storage' or 'wiki', defaults to 'storage')
            editor (str | None): The editor to use for the page (defaults to None, alternative is 'v2')
            full_width (bool): If to use full width layout (defaults to False)
            status (str): The status of the page (defaults to None, i.e. 'current')
            context (MCPContext | None): MCP context for the operation

        Raises:
            HTTPError: If the request to the Confluence API fails

        Returns:
            Response | type[Any] | bytes | str | None: JSON response containing the created page details

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
        expand: str = "space,history,body.view,metadata.labels,version",
        version: str | None = None,
        context: MCPContext | None = None,  # noqa: ARG002
    ) -> Response | type[Any] | bytes | str | None:
        """
        Get a specific Confluence page by its ID.

        Args:
            page_id (str): The ID of the page to retrieve
            status (str | None): Page status to retrieve ('current' or specific version, defaults to None, i.e. current"
                " version")
            expand (str): A comma-separated list of properties to expand in the response
                (defaults to 'space,history,body.view,metadata.labels,version')
            version (str | None): Specific version number to retrieve (optional)
            context (MCPContext | None): MCP context for the operation

        Raises:
            HTTPError: If the request to the Confluence API fails

        Returns:
            (Response | type[Any] | bytes | str | None): JSON response containing the page details

        """
        return self._api.get_page_by_id(page_id, status, expand, version)

    @mcp_tool()
    def page_update(  # noqa: PLR0913, PLR0917
        self,
        page_id: str,
        title: str,
        body: str,
        parent_id: str | None = None,
        type: str = "page",  # noqa: A002
        representation: str = "storage",
        minor_edit: bool = False,
        version_comment: str | None = None,
        always_update: bool = False,
        full_width: bool = False,
        context: MCPContext | None = None,  # noqa: ARG002
    ) -> Response | type[Any] | bytes | str | None:  # -> Response | Any | bytes | Any | None | str:
        """
        Update a Confluence page.

        Args:
            page_id (str): The ID of the page to update
            title (str): The new title for the page
            body (str): The new content/body for the page
            parent_id (str | None): The ID of the parent page if moving the page
            type (str): The type of content to update (defaults to 'page')
            representation (str): The representation of the content ('storage' or 'wiki', defaults to 'storage')
            minor_edit (bool): Whether this is a minor edit (defaults to False)
            version_comment (str | None): Optional comment to describe the change
            always_update (bool): Force update even if version conflict (defaults to False)
            full_width (bool): If to use full width layout (defaults to False)
            context (MCPContext | None): MCP context for the operation

        Raises:
            HTTPError: If the request to the Confluence API fails

        Returns:
            Response | type[Any] | bytes | str | None: JSON response containing the updated page details

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
        context: MCPContext | None = None,  # noqa: ARG002
    ) -> Response | type[Any] | bytes | str | None:
        """
        Delete a Confluence page.

        Args:
            page_id (str): The ID of the page to delete
            status (str | None): OPTIONAL: type of page
            recursive (bool): if True - will recursively delete all children pages too (defaults to False)
            context (MCPContext | None): MCP context for the operation

        Raises:
            HTTPError: If the request to the Confluence API fails

        Returns:
            Response | type[Any] | bytes | str | None: Response from the Confluence API after deleting the page

        """
        return self._api.remove_page(page_id, status, recursive)

    @mcp_tool()
    def page_list(  # noqa: PLR0913, PLR0917
        self,
        space_key: str,
        start: int = 0,
        limit: int = 1000,
        status: str | None = None,
        expand: str | None = None,
        content_type: str = "page",
        context: MCPContext | None = None,  # noqa: ARG002
    ) -> Response | type[Any] | bytes | str | None:
        """
        List pages in a Confluence space.

        Args:
            space_key (str): The key of the space to get pages from
            start (int): The starting index of the returned pages (defaults to 0)
            limit (int): Maximum number of pages to return (defaults to 1000)
            status (str | None): Filter by page status ('current' or 'archived', defaults to None, i.e. all pages)
            expand (str | None): A comma-separated list of properties to expand in the response
                (defaults to None, i.e. 'space,history,body.view,metadata.labels,version')
            content_type (str): The type of content to return (defaults to 'page')
            context (MCPContext | None): MCP context for the operation

        Raises:
            HTTPError: If the request to the Confluence API fails

        Returns:
            Response | type[Any] | bytes | str | None: List of pages in the specified space

        """
        return self._api.get_all_pages_from_space(
            space_key,
            start,
            limit,
            status,
            expand,
            content_type,
        )

    @mcp_tool()
    def page_search(  # noqa: PLR0913, PLR0917
        self,
        query: str,
        start: int = 0,
        limit: int = 1000,
        include_archived_spaces: bool = False,
        excerpt: bool = True,
        context: MCPContext | None = None,  # noqa: ARG002
    ) -> Response | type[Any] | bytes | str | None:
        """Search for pages within or across a confluence space.

        As an agent remember that the query is to be given in Confluence query language (CQL).
        E.g. 'title ~ Helmut OR text ~ Helmut' searches in those fields.
        See https://developer.atlassian.com/server/confluence/advanced-searching-using-cql
        for a definition of CQL.

        Args:
            query (str): Confluence query language (CQL) query to search for pages.
                E.g. 'title ~ Helmut OR text ~ Helmut' searches in those fields.
                See https://developer.atlassian.com/server/confluence/advanced-searching-using-cql
                for a definition of CQL.
            start (int): The starting index of the returned pages (defaults to 0)
            limit (int): Maximum number of pages to return (defaults to 1000)
            include_archived_spaces (bool): If True, include archived spaces in the search (defaults to False)
            excerpt (bool): If True, include an excerpt of the page content in the response (defaults to True)
            context (MCPContext | None): MCP context for the operation

        Raises:
            HTTPError: If the request to the Confluence API fails

        Returns:
            Response | type[Any] | bytes | str | None: List of pages in the specified space

        """
        return self._api.cql(query, start, limit, include_archived_spaces, excerpt)
