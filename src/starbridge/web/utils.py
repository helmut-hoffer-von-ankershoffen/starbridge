from urllib.parse import urlparse, urlunparse

import requests
from httpx import AsyncClient, HTTPError
from protego import Protego

from starbridge.utils import get_logger

from .types import RobotForbiddenException

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


def _get_robots_txt_url(url: str) -> str:
    """Get the robots.txt URL for a given website URL.

    Args:
        url: Website URL to get robots.txt for

    Returns:
        URL of the robots.txt file
    """
    parsed = urlparse(url)

    return urlunparse((parsed.scheme, parsed.netloc, "/robots.txt", "", "", ""))


async def ensure_allowed_to_crawl(url: str, user_agent: str) -> None:
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
                follow_redirects=True,
                headers={"User-Agent": user_agent},
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


async def get_additional_context(
    url: str,
    user_agent: str,
    accept_language: str = "en-US,en;q=0.9,de;q=0.8",
    full: bool = False,
) -> dict[str, str]:
    """Get additional context for the url.

    Args:
        url: The URL to get additional context for.

    Returns:
        additional context.
    """

    async with AsyncClient() as client:
        llms_txt = None
        if full:
            llms_full_txt_url = _get_llms_txt_url(url, True)
            try:
                response = await client.get(
                    llms_full_txt_url,
                    follow_redirects=True,
                    headers={
                        "User-Agent": user_agent,
                        "Accept-Language": accept_language,
                    },
                )
                if response.status_code == 200:
                    llms_txt = response.text
            except HTTPError:
                logger.warning(f"Failed to fetch llms-full.txt {llms_full_txt_url}")
        if llms_txt is None:
            llms_txt_url = _get_llms_txt_url(url, False)
            try:
                response = await client.get(
                    llms_txt_url,
                    follow_redirects=True,
                    headers={
                        "User-Agent": user_agent,
                        "Accept-Language": accept_language,
                    },
                )
                if response.status_code == 200:
                    llms_txt = response.text
            except HTTPError:
                logger.warning(f"Failed to fetch llms.txt {llms_txt_url}")
        if llms_txt:
            return {"llms_txt": llms_txt}
    return {}
