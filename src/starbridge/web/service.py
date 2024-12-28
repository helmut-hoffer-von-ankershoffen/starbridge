"""Handles interaction with the world wide web."""

import httpx
from bs4 import BeautifulSoup
from markdownify import markdownify

from starbridge.mcp import MCPBaseService, MCPContext, mcp_tool
from starbridge.utils import Health, get_logger

from .settings import Settings
from .types import Format
from .utils import ensure_allowed_to_crawl, get_additional_context, is_connected

logger = get_logger(__name__)

HTML_PARSER = "html.parser"


class Service(MCPBaseService):
    """Service class for web operations."""

    _settings: Settings

    def __init__(self):
        super().__init__(Settings)

    @mcp_tool()
    def health(self, context: MCPContext | None = None) -> Health:
        if not is_connected():
            return Health(
                status=Health.Status.DOWN,
                reason="No internet connection (cannot reach google.com)",
            )
        return Health(status=Health.Status.UP)

    @mcp_tool()
    def info(self, context: MCPContext | None = None) -> dict:
        """Info about web environment"""
        return {}

    @mcp_tool()
    async def get(
        self,
        url: str,
        format: Format = Format.markdown,
        accept_language: str = "en-US,en;q=0.9,de;q=0.8",
        additional_context: bool = True,
        context: MCPContext | None = None,
    ) -> dict[str, str | bytes]:
        """Fetch page from the world wide web via HTTP GET.

        Should be called by the assistant when the user asks to fetch a page from the Internet, the world wide web; asks what's on a (web) page or behind a URL; or if the user simply pastes a URL without further context.
        This includes asks about current news, or e.g. if the user simply prompts the assitant with "What's to say about <some url, with or without the protocol prefix>".

        Args:
            url (str): The URL to fetch content from
            format (Format): Format of the returned content (optional, defaults to Format.markdown):
                - Format.bytes ("bytes"): Returns binary content as-is
                - Format.unicode ("unicode"): Returns content of the response, in unicode
                - Format.html ("html"): Returns html content as a string
                - Format.markdown ("markdown"): Returns markdown generated by converting from html.
                - Format.text ("text"): Returns plain textual content extracted from html.
            accept_language (str, optional): Accept-Language header to send as part of the get request:
                - The assistant can prompt the user for the language preferred, and set this header accordingly.
            additional_context (bool, optional): Whether to include additional context in the response. Defaults to True.
            context (MCPContext | None, optional): Context object for request tracking. Defaults to None.

        Returns:
            Dict[str, Union[str, bytes, Dict]]: A dictionary containing:
                - 'content': The fetched content based on format:
                    * bytes when format is Format.bytes
                    * str when format is any other format
                - 'context': Optional dictionary with extra context (only if additional_context=True)

        Raises:
            starbridge.web.RobotForbiddenException: If we are not allowed to crawl the URL autonomously
            requests.exceptions.RequestException: If the HTTP get request failed
            ValueError: If an invalid format was passed
        """
        async with httpx.AsyncClient() as client:
            await ensure_allowed_to_crawl(url, self._settings.user_agent)
            response = await client.get(
                str(url),
                headers={
                    "User-Agent": self._settings.user_agent,
                    "Accept-Language": accept_language,
                },
                follow_redirects=True,
            )
            rtn = {}
            match format:
                case Format.bytes:
                    rtn["content"] = response.content
                case Format.unicode:
                    rtn["content"] = response.text
                case Format.html:
                    rtn["content"] = str(BeautifulSoup(response.text, HTML_PARSER))
                case Format.markdown:
                    rtn["content"] = markdownify(
                        str(BeautifulSoup(response.text, HTML_PARSER))
                    )
                case Format.text:
                    rtn["content"] = BeautifulSoup(response.text, HTML_PARSER).get_text(
                        strip=True
                    )
                case _:
                    raise ValueError(f"Invalid format: {format}")

            if additional_context:
                _context = await get_additional_context(
                    url, self._settings.user_agent, accept_language
                )
                if _context:
                    rtn["context"] = _context
            return rtn