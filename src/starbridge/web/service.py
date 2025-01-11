"""Handles interaction with the world wide web."""

from starbridge.mcp import MCPBaseService, MCPContext, mcp_tool
from starbridge.utils import Health, get_logger

from .models import GetResult
from .settings import Settings
from .utils import (
    extract_links_from_response,
    get_additional_context_for_url,
    get_respectfully,
    is_connected,
    transform_content,
)

logger = get_logger(__name__)


class Service(MCPBaseService):
    """Service class for web operations."""

    _settings: Settings

    def __init__(self) -> None:
        """Initialize the web service with default settings."""
        super().__init__(Settings)

    @mcp_tool()
    def health(self, context: MCPContext | None = None) -> Health:  # noqa: PLR6301, ARG002
        """
        Check health of the web service.

        Args:
            context (MCPContext | None): MCP context for the operation

        Returns:
            Health: The health status of the web service

        """
        if not is_connected():
            return Health(
                status=Health.Status.DOWN,
                reason="No internet connection (cannot reach google.com)",
            )
        return Health(status=Health.Status.UP)

    @mcp_tool()
    def info(self, context: MCPContext | None = None) -> dict:  # noqa: PLR6301, ARG002
        """
        Info about web environment.

        Args:
            context (MCPContext | None): MCP context for the operation

        Returns:
            dict: Information about the web environment

        """
        return {}

    @mcp_tool()
    async def get(  # noqa: PLR0913, PLR0917
        self,
        url: str,
        accept_language: str = "en-US,en;q=0.9,de;q=0.8",
        transform_to_markdown: bool = True,
        extract_links: bool = True,
        additional_context: bool = True,
        llms_full_txt: bool = False,
        force_not_respecting_robots_txt: bool = False,
        context: MCPContext | None = None,  # noqa: ARG002
    ) -> GetResult:
        """
        Fetch page from the world wide web via HTTP GET.

        Should be called by the assistant when the user asks to fetch/retrieve/load/download
            a page/content/document from
        the Internet / the world wide web
            - This includes the case when the user simply pastes a URL without further context
            - This includes asks about current news, or e.g. if the user simply prompts the assitant with
                "What's today on <some website>".
            - This includes asks to download a pdf
        Further tips:
            - The agent is to disable transform to markdown, extract links, and additional context in error cases only.
            - The agent can use this tool to crawl multiple pages. I.e. when asked to crawl a URL use a get call, than
                look at the top links extracted, follow them, and in the end provide a summary.

        Args:
            url (str): The URL to fetch content from
            accept_language (str, optional): Accept-Language header to send as part of the get request.
                Defaults to en-US,en;q=0.9,de;q=0.8.
                The assistant can prompt the user for the language preferred, and set this header accordingly.
            transform_to_markdown (bool, optional): If set will transform content to markdown if possible.
                Defaults to true. If the transformation is not supported, the content will be returned as is
            extract_links (bool, optional): If set will extract links from the content. Defaults to True.
                Supported for selected content types only
            additional_context (bool, optional): If set will include additional context about the URL
                or it's domain in the response. Defaults to True.
            llms_full_txt (bool, optional): Whether to include llms-full.txt in additional context. Defaults to False.
            force_not_respecting_robots_txt (bool, optional): Whether to **not** check robots.txt.
                If True, the agent will ignore robots.txt.
                If False, the agent will respect robots.txt if the environment variable
                STARBRIDGE_WEB_RESPPECT_ROBOTS_TXT is set to 1.
                Defaults to False.
            context (MCPContext | None, optional): Context object for request tracking. Defaults to None.

        Returns:
            'resource': The retrieved and possibly transformed resource:
                - 'url' (string) the final URL after redirects
                - 'type' (content type indicator as defined in http): the type of transformed content,
                    resp. the original
                    content type if no transformation applied
                - 'text' (string): the transformed textual content, resp. the original content if no transformation
                    applied
                - 'blob' (bytes): the binary content of the resource, if the resource has binary content
            'extracted_links': Optional list of links extracted from the resource, if extract_links=True.
                Sorted by number of occurrences of a URL in the resource. Each item has:
                - 'url' (string) the URL of the link
                - 'occurrences' (int) the number of occurrences of the link in the resource
                - 'anchor_texts' (list of strings) the anchor texts of the link
            'additional_context': Optional list of with extra context (only if additional_context=True). Each item has:
                - 'url' (string) the URL of the context
                - 'type' (string) the type of context, e.g. llms_txt for text specifally prepared by a domain for an
                    assistant to read
                - 'text' (string) the content of the context in markdown format

        Raises:
            starbridge.web.RobotForbiddenError: If we are not allowed to crawl the URL autonomously
            requests.exceptions.RequestException: If the HTTP get request failed
            ValueError: If an invalid format was passed

        """
        response = await get_respectfully(
            url=url,
            respect_robots_txt=(not force_not_respecting_robots_txt) and self._settings.respect_robots_txt,
            user_agent=self._settings.user_agent,
            accept_language=accept_language,
            timeout=self._settings.timeout,
        )
        rtn = GetResult(resource=transform_content(response, transform_to_markdown))

        if extract_links:
            rtn.extracted_links = extract_links_from_response(response)

        if additional_context:
            rtn.additional_context = await get_additional_context_for_url(
                url=url,
                user_agent=self._settings.user_agent,
                accept_language=accept_language,
                timeout=self._settings.timeout,
                full=llms_full_txt,
            )

        return rtn
