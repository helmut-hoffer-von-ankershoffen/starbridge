import asyncio
from unittest.mock import patch

import pytest
from httpx import TimeoutException
from nox import project

from starbridge import __project_name__
from starbridge.web import RobotForbiddenException
from starbridge.web.utils import ensure_allowed_to_crawl, get_additional_context

GET_TEST_URL = "https://helmuthva.gitbook.io/starbridge"
HTTPX_ASYNC_CLIENT_GET = "httpx.AsyncClient.get"
TIMEOUT_MESSAGE = "Connection timed out"
LLMS_TXT_URL = "https://docs.anthropic.com"
LLMS_TXT = "llms_txt"
LLMS_FULL_TXT = "llms-full.txt"
LLMS_DUMY_CONTENT = "llms content"


def test_web_util_ensure_allowed_to_crawl_forbidden_on_timeout():
    """Check web info."""

    with pytest.raises(RobotForbiddenException):
        with patch(HTTPX_ASYNC_CLIENT_GET) as mock_get:
            mock_get.side_effect = TimeoutException(TIMEOUT_MESSAGE)
            asyncio.run(ensure_allowed_to_crawl(GET_TEST_URL, __project_name__))


def test_web_util_ensure_allowed_to_crawl_forbidden_on_401():
    """Check web info."""

    with pytest.raises(RobotForbiddenException):
        with patch(HTTPX_ASYNC_CLIENT_GET) as mock_get:
            mock_get.return_value.status_code = 401
            asyncio.run(ensure_allowed_to_crawl(GET_TEST_URL, __project_name__))


def test_web_util_ensure_allowed_to_crawl_allowed_on_404():
    """Check web info."""

    with patch(HTTPX_ASYNC_CLIENT_GET) as mock_get:
        mock_get.return_value.status_code = 404
        # No exception should be raised
        asyncio.run(ensure_allowed_to_crawl(GET_TEST_URL, __project_name__))


def test_web_get_additional_context_success():
    """Check web info."""

    context = asyncio.run(get_additional_context(LLMS_TXT_URL, __project_name__))
    assert LLMS_TXT in context


def test_web_get_additional_context_empty_on_404():
    """Check web info."""

    with patch(HTTPX_ASYNC_CLIENT_GET) as mock_get:
        mock_get.return_value.status_code = 404
        # No exception should be raised
        context = asyncio.run(get_additional_context(LLMS_TXT_URL, __project_name__))
        assert LLMS_TXT not in context


def test_web_get_additional_context_empty_on_timeout():
    """Check web info."""

    with patch(HTTPX_ASYNC_CLIENT_GET) as mock_get:
        mock_get.side_effect = TimeoutException(TIMEOUT_MESSAGE)
        # No exception should be raised
        context = asyncio.run(get_additional_context(LLMS_TXT_URL, __project_name__))
        assert LLMS_TXT not in context


def test_web_get_additional_context_empty_on_full_timeout():
    """Check web info."""

    with patch(HTTPX_ASYNC_CLIENT_GET) as mock_get:
        mock_get.side_effect = TimeoutException(TIMEOUT_MESSAGE)
        # No exception should be raised
        context = asyncio.run(
            get_additional_context(LLMS_TXT_URL, __project_name__, full=True)
        )
        assert LLMS_TXT not in context


def test_web_get_additional_context_fallback_to_non_full():
    """Check web info."""

    class MockResponse:
        def __init__(self, status_code, text=""):
            self.status_code = status_code
            self.text = text

    def mock_get_side_effect(url, **kwargs):
        if LLMS_FULL_TXT in url:
            return MockResponse(404)
        return MockResponse(200, LLMS_DUMY_CONTENT)

    with patch(HTTPX_ASYNC_CLIENT_GET) as mock_get:
        mock_get.side_effect = mock_get_side_effect
        context = asyncio.run(
            get_additional_context(LLMS_TXT_URL, __project_name__, full=True)
        )
        assert LLMS_TXT in context
        assert context[LLMS_TXT] == LLMS_DUMY_CONTENT


def test_web_get_additional_context_empty_on():
    """Check web info."""

    class MockResponse:
        def __init__(self, status_code, text=""):
            self.status_code = status_code
            self.text = text

    def mock_get_side_effect(url, **kwargs):
        if LLMS_FULL_TXT in url:
            return MockResponse(404)
        return MockResponse(200, LLMS_DUMY_CONTENT)

    with patch(HTTPX_ASYNC_CLIENT_GET) as mock_get:
        mock_get.side_effect = mock_get_side_effect
        context = asyncio.run(
            get_additional_context(LLMS_TXT_URL, __project_name__, full=True)
        )
        assert LLMS_TXT in context
        assert context[LLMS_TXT] == LLMS_DUMY_CONTENT
