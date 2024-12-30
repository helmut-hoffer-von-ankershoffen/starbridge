from urllib.parse import urljoin, urlparse, urlunparse

import httpx
import markdown
import requests
from bs4 import BeautifulSoup
from httpx import AsyncClient, HTTPError
from markdownify import ATX, MarkdownConverter, markdownify
from markitdown import MarkItDown
from protego import Protego
from pydantic import AnyHttpUrl
from readabilipy.simple_json import simple_json_from_html_string

from starbridge.utils import get_logger

from .types import (
    HTML_PARSER,
    Context,
    LinkTarget,
    MimeType,
    Resource,
    RobotForbiddenException,
)

logger = get_logger(__name__)


def is_connected():
    try:
        response = requests.head("https://www.google.com", timeout=5)
        logger.info(
            "Called head on https://www.google.com/, got status_code: %s",
            response.status_code,
        )
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        logger.error("Failed to connect to www.google.com: %s", e)
    return False


async def get_respectfully(
    url: str,
    user_agent: str,
    accept_language: str,
    timeout: int,
    respect_robots_txt: bool = True,
) -> httpx.Response:
    """Fetch URL with proper headers and robot.txt checking."""
    async with AsyncClient() as client:
        if respect_robots_txt:
            await _ensure_allowed_to_crawl(url=url, user_agent=user_agent)

        response = await client.get(
            str(url),
            headers={
                "User-Agent": user_agent,
                "Accept-Language": accept_language,
            },
            follow_redirects=True,
            timeout=timeout,
        )
        return response


def _get_robots_txt_url(url: str) -> str:
    """Get the robots.txt URL for a given website URL.

    Args:
        url: Website URL to get robots.txt for

    Returns:
        URL of the robots.txt file
    """
    parsed = urlparse(url)

    return urlunparse((parsed.scheme, parsed.netloc, "/robots.txt", "", "", ""))


async def _ensure_allowed_to_crawl(url: str, user_agent: str, timeout: int = 5) -> None:
    """
    Ensure allowed to crawl the URL by the user agent according to the robots.txt file.
    Raises a RuntimeError if not.
    """

    logger.debug("Checking if allowed to crawl %s", url)
    robot_txt_url = _get_robots_txt_url(url)

    async with AsyncClient() as client:
        try:
            response = await client.get(
                robot_txt_url,
                headers={"User-Agent": user_agent},
                follow_redirects=True,
                timeout=timeout,
            )
        except HTTPError as e:
            message = f"Failed to fetch robots.txt {robot_txt_url} due to a connection issue, thereby defensively assuming we are not allowed to access the url we want."
            logger.error(message)
            raise RobotForbiddenException(message) from e
        if response.status_code in (401, 403):
            message = (
                f"When fetching robots.txt ({robot_txt_url}), received status {response.status_code} so assuming that autonomous fetching is not allowed, the user can try manually fetching by using the fetch prompt",
            )
            logger.error(message)
            raise RobotForbiddenException(message)
        elif 400 <= response.status_code < 500:
            return
        robot_txt = response.text
    processed_robot_txt = "\n".join(
        line for line in robot_txt.splitlines() if not line.strip().startswith("#")
    )
    robot_parser = Protego.parse(processed_robot_txt)
    if not robot_parser.can_fetch(str(url), user_agent):
        message = (
            f"The sites robots.txt ({robot_txt_url}), specifies that autonomous fetching of this page is not allowed, "
            f"<useragent>{user_agent}</useragent>\n"
            f"<url>{url}</url>\n"
            f"<robots>\n{robot_txt}\n</robots>\n"
            f"The assistant must let the user know that it failed to view the page. The assistant may provide further guidance based on the above information.\n"
            f"The assistant can tell the user that they can try manually fetching the page by using the fetch prompt within their UI.",
        )
        logger.error(message)
        raise RobotForbiddenException(message)


def _get_normalized_content_type(response: httpx.Response) -> str:
    """Get the normalized content type from the response."""

    content_type_mapping = {
        "html": MimeType.TEXT_HTML,
        "markdown": MimeType.TEXT_MARKDWON,
        "text": MimeType.TEXT_PLAIN,
        "pdf": MimeType.APPLICATION_PDF,
        MimeType.APPLICATION_OPENXML_WORD: MimeType.APPLICATION_OPENXML_WORD,
        MimeType.APPLICATION_OPENXML_EXCEL: MimeType.APPLICATION_OPENXML_EXCEL,
    }

    extension_mapping = {
        (".html", ".htm"): MimeType.TEXT_HTML,
        (".md",): MimeType.TEXT_MARKDWON,
        (".txt",): MimeType.TEXT_PLAIN,
        (".pdf",): MimeType.APPLICATION_PDF,
        (".docx",): MimeType.APPLICATION_OPENXML_WORD,
        (".xlsx",): MimeType.APPLICATION_OPENXML_EXCEL,
    }

    content_type = response.headers.get("content-type", "").lower()
    for key, mime_type in content_type_mapping.items():
        if key in content_type:
            return mime_type

    url = str(response.url).lower()
    for extensions, mime_type in extension_mapping.items():
        if any(url.endswith(ext) for ext in extensions):
            return mime_type

    return content_type


def _get_markdown_from_html(html: str) -> str:
    """Get markdown from HTML content."""
    simplified = simple_json_from_html_string(html, use_readability=False)
    if simplified["content"]:
        return markdownify(simplified["content"], heading_style=ATX, strip=["img"])
    return MarkdownConverter(heading_style=ATX, strip=["img"]).convert_soup(
        BeautifulSoup(html, HTML_PARSER)
    )


def _get_markdown_from_pdf(response: httpx.Response) -> str | None:
    """Get markdown from PDF content."""
    try:
        rtn = MarkItDown().convert(str(response.url))
        return rtn.text_content
    except Exception as e:
        logger.warning(f"Failed to convert PDF to markdown: {e}")
        return None


def _get_markdown_from_word(response: httpx.Response) -> str | None:
    try:
        rtn = MarkItDown().convert(str(response.url))
        return rtn.text_content
    except Exception as e:
        logger.warning(f"Failed to convert PDF to markdown: {e}")
        return None


def _get_markdown_from_excel(response: httpx.Response) -> str | None:
    try:
        rtn = MarkItDown().convert(str(response.url))
        return rtn.text_content
    except Exception as e:
        logger.warning(f"Failed to convert PDF to markdown: {e}")
        return None


def transform_content(
    response: httpx.Response, transform_to_markdown: bool = True
) -> Resource:
    """Process response according to requested format."""
    content_type = _get_normalized_content_type(response)

    if transform_to_markdown:
        match content_type:
            case MimeType.TEXT_HTML:
                return Resource(
                    url=AnyHttpUrl(str(response.url)),
                    type=MimeType.TEXT_MARKDWON,
                    text=_get_markdown_from_html(response.text),
                )
            case MimeType.APPLICATION_PDF:
                md = _get_markdown_from_pdf(response)
                if md:
                    return Resource(
                        url=AnyHttpUrl(str(response.url)),
                        type=MimeType.TEXT_MARKDWON,
                        text=md,
                    )
            case MimeType.APPLICATION_OPENXML_WORD:
                md = _get_markdown_from_word(response)
                if md:
                    return Resource(
                        url=AnyHttpUrl(str(response.url)),
                        type=MimeType.TEXT_MARKDWON,
                        text=md,
                    )
            case MimeType.APPLICATION_OPENXML_EXCEL:
                md = _get_markdown_from_excel(response)
                if md:
                    return Resource(
                        url=AnyHttpUrl(str(response.url)),
                        type=MimeType.TEXT_MARKDWON,
                        text=md,
                    )

    if any(
        mime_type in content_type
        for mime_type in [
            MimeType.TEXT_PLAIN,
            MimeType.TEXT_MARKDWON,
            MimeType.TEXT_HTML,
        ]
    ):
        return Resource(
            url=AnyHttpUrl(str(response.url)),
            type=content_type,
            text=response.text,
        )
    return Resource(
        url=AnyHttpUrl(str(response.url)),
        type=content_type,
        blob=response.content,
    )


def _extract_links_from_html(html: str, url: str) -> list[LinkTarget]:
    """Extract links from HTML content."""
    soup = BeautifulSoup(html, HTML_PARSER)
    seen_urls: dict[str, LinkTarget] = {}

    for link in soup.find_all("a", href=True):
        href = link.get("href")
        abs_url = urljoin(url, href)
        if abs_url.startswith(("http://", "https://")):  # ignore non-http(s) links
            anchor_text = link.get_text().strip()
            if not anchor_text:
                continue
            if abs_url in seen_urls:
                if anchor_text not in seen_urls[abs_url].anchor_texts:
                    seen_urls[abs_url].anchor_texts.append(anchor_text)
                seen_urls[abs_url].occurrences += 1
            else:
                seen_urls[abs_url] = LinkTarget(
                    url=AnyHttpUrl(abs_url), occurrences=1, anchor_texts=[anchor_text]
                )

    # Sort by occurrences in descending order
    return sorted(seen_urls.values(), key=lambda x: x.occurrences, reverse=True)


def extract_links_from_response(
    response: httpx.Response,
) -> list[LinkTarget]:
    """Extract links from HTML content."""

    match _get_normalized_content_type(response):
        case MimeType.TEXT_HTML:
            return _extract_links_from_html(response.text, str(response.url))
        case MimeType.TEXT_MARKDWON:
            return _extract_links_from_html(
                markdown.markdown(response.text), str(response.url)
            )
        case _:
            return []


async def get_additional_context_for_url(
    url: str,
    user_agent: str,
    accept_language: str = "en-US,en;q=0.9,de;q=0.8",
    timeout: int = 5,
    full: bool = False,
) -> list[Context]:
    """Get additional context for the url.

    Args:
        url: The URL to get additional context for.

    Returns:
        additional context.
    """
    _rtn = []
    async with AsyncClient() as client:
        if full:
            llms_full_txt_url = _get_llms_txt_url(url, True)
            try:
                response = await client.get(
                    llms_full_txt_url,
                    headers={
                        "User-Agent": user_agent,
                        "Accept-Language": accept_language,
                    },
                    follow_redirects=True,
                    timeout=timeout,
                )
                if response.status_code == 200:
                    _rtn.append(
                        Context(
                            type="llms_txt",
                            url=AnyHttpUrl(llms_full_txt_url),
                            text=response.text,
                        )
                    )
            except HTTPError:
                logger.warning(f"Failed to fetch llms-full.txt {llms_full_txt_url}")
        if len(_rtn) == 0:
            llms_txt_url = _get_llms_txt_url(url, False)
            try:
                response = await client.get(
                    llms_txt_url,
                    headers={
                        "User-Agent": user_agent,
                        "Accept-Language": accept_language,
                    },
                    follow_redirects=True,
                    timeout=timeout,
                )
                if response.status_code == 200:
                    _rtn.append(
                        Context(
                            type="llms_txt",
                            url=AnyHttpUrl(llms_txt_url),
                            text=response.text,
                        )
                    )
            except HTTPError:
                logger.warning(f"Failed to fetch llms.txt {llms_txt_url}")
    return _rtn


def _get_llms_txt_url(url: str, full: bool = True) -> str:
    """Get the llms.txt resp. llms-full.txt URL for a given website URL.

    Args:
        url: Website URL to get robots.txt for

    Returns:
        URL of the robots.txt file
    """
    parsed = urlparse(url)

    if full:
        return urlunparse((parsed.scheme, parsed.netloc, "/llms-full.txt", "", "", ""))
    return urlunparse((parsed.scheme, parsed.netloc, "/llms.txt", "", "", ""))
