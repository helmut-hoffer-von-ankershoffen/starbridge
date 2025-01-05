"""Handles search interactions."""

import asyncio

from brave_search_python_client import (
    BraveSearch,
    WebSearchApiResponse,
    WebSearchRequest,
)

from starbridge.mcp import MCPBaseService, MCPContext, mcp_tool
from starbridge.utils import Health, get_logger

from .settings import Settings

logger = get_logger(__name__)


class Service(MCPBaseService):
    """Service class for search operations."""

    _settings: Settings
    _bs: BraveSearch

    def __init__(self) -> None:
        """Initialize the search service with Brave Search client."""
        super().__init__(Settings)
        self._bs = BraveSearch(api_key=self._settings.brave_search_api_key)

    @mcp_tool()
    def health(self, context: MCPContext | None = None) -> Health:  # noqa: ARG002
        """
        Check health of the search service.

        Args:
            context (MCPContext | None): MCP context for the operation

        Returns:
            Health: The health status of the search service.

        """
        if not asyncio.run(self._bs.is_connected()):
            return Health(
                status=Health.Status.DOWN,
                reason="Brave Search API not connected",
            )
        return Health(status=Health.Status.UP)

    @mcp_tool()
    def info(self, context: MCPContext | None = None) -> dict:  # noqa: ARG002, PLR6301
        """
        Info about search environment.

        Args:
            context (MCPContext | None): MCP context for the

        Returns:
            dict: Information about the search environment configuration.

        """
        return {}

    @mcp_tool()
    async def web(  # noqa: D417
        self,
        q: str,
        context: MCPContext | None = None,  # noqa: ARG002
    ) -> WebSearchApiResponse:
        """
        Search the world wide web via Brave Search.

        Should be called by the assistant when the user asks to search the Internet / the world wide web
            - This includes the case when the user asks to find something in the web

        Args:
            q (str): The query to search for

        Returns:
            (WebSearchApiResponse): JSON response containing search results returned by Brave Search API

        Raises:
            (BraveSearchClientError): If the request was formulated wrong
            (BraveSearchApiError): If the Brave Search API was not reachable or had an internal server error

        """
        return await self._bs.web(WebSearchRequest(q=q))
