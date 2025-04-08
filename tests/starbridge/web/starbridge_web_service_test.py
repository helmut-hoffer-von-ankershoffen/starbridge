"""Tests for the web service functionality."""

import asyncio
from unittest.mock import patch

import pytest

from starbridge.web import RobotForbiddenError, Service

GET_TEST_TEXT_URL = (
    "https://github.com/helmut-hoffer-von-ankershoffen/starbridge/raw/refs/heads/main/tests/fixtures/starbridge.txt"
)
GET_TEST_MARKDOWN_URL = (
    "https://github.com/helmut-hoffer-von-ankershoffen/starbridge/raw/refs/heads/main/tests/fixtures/starbridge.md"
)
GET_TEST_PDF_URL = (
    "https://github.com/helmut-hoffer-von-ankershoffen/starbridge/raw/refs/heads/main/tests/fixtures/starbridge.pdf"
)
GET_TEST_WORD_URL = (
    "https://github.com/helmut-hoffer-von-ankershoffen/starbridge/raw/refs/heads/main/tests/fixtures/starbridge.docx"
)
GET_TEST_EXCEL_URL = (
    "https://github.com/helmut-hoffer-von-ankershoffen/starbridge/raw/refs/heads/main/tests/fixtures/starbridge.xlsx"
)


def test_web_service_get_forbidden() -> None:
    """Check getting content from the web fails if forbidden by robots.txt."""
    from starbridge.web import Service

    with pytest.raises(RobotForbiddenError):
        asyncio.run(Service().get("https://github.com/search/advanced"))


@patch(
    "starbridge.web.utils._ensure_allowed_to_crawl",
    return_value=None,
)
@pytest.mark.asyncio
async def test_web_service_get_pdf(runner) -> None:
    """Check getting content from the web as markdown."""
    result = await Service().get(
        url=GET_TEST_PDF_URL,
    )
    assert "Hello World" in (result.resource.text or "")


@patch(
    "starbridge.web.utils._ensure_allowed_to_crawl",
    return_value=None,
)
@pytest.mark.asyncio
async def test_web_service_get_word(runner) -> None:
    """Check getting content from the web as markdown."""
    result = await Service().get(
        url=GET_TEST_WORD_URL,
    )
    assert "# Headline" in (result.resource.text or "")


@patch(
    "starbridge.web.utils._ensure_allowed_to_crawl",
    return_value=None,
)
@pytest.mark.asyncio
async def test_web_service_get_excel(runner) -> None:
    """Check getting content from the web as markdown."""
    result = await Service().get(
        url=GET_TEST_EXCEL_URL,
    )
    assert "Starbridge" in (result.resource.text or "")


@patch(
    "starbridge.web.utils._ensure_allowed_to_crawl",
    return_value=None,
)
@pytest.mark.asyncio
async def test_web_service_get_text(runner) -> None:
    """Check getting content from the web as markdown."""
    result = await Service().get(
        url=GET_TEST_TEXT_URL,
    )
    assert "Lorem Ipsum" in (result.resource.text or "")


@patch(
    "starbridge.web.utils._ensure_allowed_to_crawl",
    return_value=None,
)
@pytest.mark.asyncio
async def test_web_service_get_markdown(runner) -> None:
    """Check getting content from the web as markdown."""
    result = await Service().get(
        url=GET_TEST_MARKDOWN_URL,
    )
    assert "Lorem Ipsum" in (result.resource.text or "")
