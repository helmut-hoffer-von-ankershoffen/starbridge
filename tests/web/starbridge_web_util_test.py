import asyncio
from unittest.mock import patch

import pytest
from httpx import TimeoutException

from starbridge.web import RobotForbiddenException
from starbridge.web.utils import ensure_allowed_to_crawl, get_additional_context

GET_TEST_URL = "https://helmuthva.gitbook.io/starbridge"


def test_web_util_ensure_allowed_to_crawl_forbidden_on_timeout():
    """Check web info."""

    with pytest.raises(RobotForbiddenException):
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_get.side_effect = TimeoutException("Connection timed out")
            asyncio.run(ensure_allowed_to_crawl("https://www.google.com", "starbridge"))


def test_web_util_ensure_allowed_to_crawl_forbidden_on_401():
    """Check web info."""

    with pytest.raises(RobotForbiddenException):
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_get.return_value.status_code = 401
            asyncio.run(ensure_allowed_to_crawl("https://www.google.com", "starbridge"))


def test_web_util_ensure_allowed_to_crawl_allowed_on_404():
    """Check web info."""

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value.status_code = 404
        # No exception should be raised
        asyncio.run(ensure_allowed_to_crawl("https://www.google.com", "starbridge"))


def test_web_get_additional_context_success():
    """Check web info."""

    context = asyncio.run(
        get_additional_context("https://docs.anthropic.com", "starbridge")
    )
    assert "llms_txt" in context


def test_web_get_additional_context_empty_on_404():
    """Check web info."""

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value.status_code = 404
        # No exception should be raised
        context = asyncio.run(
            get_additional_context("https://docs.anthropic.com", "starbridge")
        )
        assert "llms_txt" not in context


def test_web_get_additional_context_empty_on_timeout():
    """Check web info."""

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.side_effect = TimeoutException("Connection timed out")
        # No exception should be raised
        context = asyncio.run(
            get_additional_context("https://docs.anthropic.com", "starbridge")
        )
        assert "llms_txt" not in context


def test_web_get_additional_context_empty_on_full_timeout():
    """Check web info."""

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.side_effect = TimeoutException("Connection timed out")
        # No exception should be raised
        context = asyncio.run(
            get_additional_context(
                "https://docs.anthropic.com", "starbridge", full=True
            )
        )
        assert "llms_txt" not in context


def test_web_get_additional_context_fallback_to_non_full():
    """Check web info."""

    class MockResponse:
        def __init__(self, status_code, text=""):
            self.status_code = status_code
            self.text = text

    def mock_get_side_effect(url, **kwargs):
        if "llms-full.txt" in url:
            return MockResponse(404)
        return MockResponse(200, "llms content")

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.side_effect = mock_get_side_effect
        context = asyncio.run(
            get_additional_context(
                "https://docs.anthropic.com", "starbridge", full=True
            )
        )
        assert "llms_txt" in context
        assert context["llms_txt"] == "llms content"


def test_web_get_additional_context_empty_on():
    """Check web info."""

    class MockResponse:
        def __init__(self, status_code, text=""):
            self.status_code = status_code
            self.text = text

    def mock_get_side_effect(url, **kwargs):
        if "llms-full.txt" in url:
            return MockResponse(404)
        return MockResponse(200, "llms content")

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.side_effect = mock_get_side_effect
        context = asyncio.run(
            get_additional_context(
                "https://docs.anthropic.com", "starbridge", full=True
            )
        )
        assert "llms_txt" in context
        assert context["llms_txt"] == "llms content"
