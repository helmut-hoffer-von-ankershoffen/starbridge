"""Tests for web utilities functionality."""

import asyncio
from unittest.mock import patch

import pytest
from httpx import TimeoutException

from starbridge import __project_name__
from starbridge.web import RobotForbiddenError
from starbridge.web.utils import (
    _ensure_allowed_to_crawl,
    get_additional_context_for_url,
)

GET_TEST_URL = "https://starbridge.readthedocs.io/en/latest/"
HTTPX_ASYNC_CLIENT_GET = "httpx.AsyncClient.get"
TIMEOUT_MESSAGE = "Connection timed out"
LLMS_TXT_URL = "https://docs.anthropic.com"
LLMS_TXT = "llms_txt"
LLMS_FULL_TXT = "llms-full.txt"
LLMS_DUMY_CONTENT = "llms content"


def test_web_utils_robots_disallowed_on_timeout() -> None:
    """Check disallowing on robots.txt timing out."""
    with pytest.raises(RobotForbiddenError), patch(HTTPX_ASYNC_CLIENT_GET) as mock_get:
        mock_get.side_effect = TimeoutException(TIMEOUT_MESSAGE)
        asyncio.run(_ensure_allowed_to_crawl(GET_TEST_URL, __project_name__))


def test_web_utils_robots_disallowed_on_401() -> None:
    """Check disallowing on robots.txt forbidden."""
    with pytest.raises(RobotForbiddenError), patch(HTTPX_ASYNC_CLIENT_GET) as mock_get:
        mock_get.return_value.status_code = 401
        asyncio.run(_ensure_allowed_to_crawl(GET_TEST_URL, __project_name__))


def test_web_utils_robots_allowed_on_404() -> None:
    """Check allowing on robots.txt not found."""
    with patch(HTTPX_ASYNC_CLIENT_GET) as mock_get:
        mock_get.return_value.status_code = 404
        # No exception should be raised
        asyncio.run(_ensure_allowed_to_crawl(GET_TEST_URL, __project_name__))


def test_web_utils_context_success() -> None:
    """Check context includes llms_txt if exists."""
    context = asyncio.run(
        get_additional_context_for_url(LLMS_TXT_URL, __project_name__),
    )
    assert any(ctx.type == "llms_txt" for ctx in context)


def test_web_utils_context_empty_on_404() -> None:
    """Check context empty if llms.txt not found."""
    with patch(HTTPX_ASYNC_CLIENT_GET) as mock_get:
        mock_get.return_value.status_code = 404
        # No exception should be raised
        context = asyncio.run(
            get_additional_context_for_url(LLMS_TXT_URL, __project_name__),
        )
        assert len(context) == 0


def test_web_utils_context_empty_on_timeout() -> None:
    """Check context empty on download of llms.txt timeout."""
    with patch(HTTPX_ASYNC_CLIENT_GET) as mock_get:
        mock_get.side_effect = TimeoutException(TIMEOUT_MESSAGE)
        # No exception should be raised
        context = asyncio.run(
            get_additional_context_for_url(LLMS_TXT_URL, __project_name__),
        )
        assert len(context) == 0


def test_web_utils_context_empty_on_full_timeout() -> None:
    """Check context empty on download of llms-full.txt and llms.txt timeout."""
    with patch(HTTPX_ASYNC_CLIENT_GET) as mock_get:
        mock_get.side_effect = TimeoutException(TIMEOUT_MESSAGE)
        # No exception should be raised
        context = asyncio.run(
            get_additional_context_for_url(LLMS_TXT_URL, __project_name__, full=True),
        )
        assert len(context) == 0


def test_web_utils_context_fallback_to_non_full() -> None:
    """Check context contains llms.txt even if llms-full.txt not found."""

    class MockResponse:
        def __init__(self, status_code, text="") -> None:
            self.status_code = status_code
            self.text = text

    def mock_get_side_effect(url, **kwargs):
        if LLMS_FULL_TXT in url:
            return MockResponse(404)
        return MockResponse(200, LLMS_DUMY_CONTENT)

    with patch(HTTPX_ASYNC_CLIENT_GET) as mock_get:
        mock_get.side_effect = mock_get_side_effect
        context = asyncio.run(
            get_additional_context_for_url(LLMS_TXT_URL, __project_name__, full=True),
        )
        assert len(context) >= 1
        llms_txt_context = next(
            (ctx for ctx in context if ctx.type == "llms_txt"),
            None,
        )
        assert llms_txt_context is not None
        assert str(llms_txt_context.url) == "https://docs.anthropic.com/llms.txt"
        assert llms_txt_context.text == LLMS_DUMY_CONTENT
