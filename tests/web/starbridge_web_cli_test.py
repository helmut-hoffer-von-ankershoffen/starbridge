"""Tests for web CLI functionality."""

import json
from unittest.mock import patch

import httpx
import pytest
from typer.testing import CliRunner

from starbridge.cli import cli
from starbridge.web import GetResult

GET_TEST_HTML_URL = "https://starbridge.readthedocs.io/en/latest/"
GET_LLMS_TXT_URL = "https://docs.anthropic.com"


@pytest.fixture
def runner() -> CliRunner:
    """Get a Click CLI test runner."""
    return CliRunner()


def test_web_cli_info(runner) -> None:
    """Check web info."""
    result = runner.invoke(cli, ["web", "info"])
    assert result.exit_code == 0


def test_web_cli_health(runner) -> None:
    """Check web health."""
    result = runner.invoke(cli, ["web", "health"])
    assert '"UP"' in result.output
    assert result.exit_code == 0


@patch("httpx.head")
def test_web_cli_health_not_connected(mock_head, runner) -> None:
    """Check web health down when not connected."""
    mock_head.side_effect = httpx.TimeoutException("timeout")

    result = runner.invoke(cli, ["web", "health"])
    assert '"DOWN"' in result.output
    assert result.exit_code == 0


@patch("httpx.AsyncClient.get")
def test_web_cli_get_timeouts(mock_get, runner) -> None:
    """Check getting content fails."""
    mock_get.side_effect = httpx.TimeoutException("timeout")

    result = runner.invoke(
        cli,
        [
            "web",
            "get",
            GET_TEST_HTML_URL,
        ],
    )
    assert "Failed to fetch robots.txt" in result.output
    assert result.exit_code == 1


def test_web_cli_get_html_no_transform_works(runner) -> None:
    """Check getting content from the web as html encoded in unicode."""
    result = runner.invoke(
        cli,
        [
            "web",
            "get",
            "--no-transform-to-markdown",
            GET_TEST_HTML_URL,
        ],
    )
    rtn = GetResult.model_validate(json.loads(result.output))
    assert (rtn.resource.text or "").startswith("<!doctype html>")
    assert rtn.get_link_count() > 0
    assert result.exit_code == 0


def test_web_cli_get_html_no_transform_no_links(runner) -> None:
    """Check getting content from the web as html encoded in unicode, without extracting links."""
    result = runner.invoke(
        cli,
        [
            "web",
            "get",
            "--no-transform-to-markdown",
            "--no-extract-links",
            GET_TEST_HTML_URL,
        ],
    )
    rtn = GetResult.model_validate(json.loads(result.output))
    assert (rtn.resource.text or "").startswith("<!doctype html>")
    assert rtn.get_link_count() == 0
    assert result.exit_code == 0


def test_web_cli_get_html_to_markdown(runner) -> None:
    """Check getting content from the web as markdown."""
    result = runner.invoke(
        cli,
        [
            "web",
            "get",
            GET_TEST_HTML_URL,
        ],
    )
    rtn = GetResult.model_validate(json.loads(result.output))
    assert "starbridge " in (rtn.resource.text or "")
    assert result.exit_code == 0


def test_web_cli_get_french(runner) -> None:
    """Check getting content from the web in french."""
    result = runner.invoke(
        cli,
        [
            "web",
            "get",
            "--accept-language",
            "fr_FR",
            "https://www.google.com",
        ],
    )
    rtn = GetResult.model_validate(json.loads(result.output))
    assert "Recherche" in (rtn.resource.text or "")
    assert result.exit_code == 0


def test_web_cli_get_additional_context_llms_text(runner) -> None:
    """Check getting additional context."""
    result = runner.invoke(
        cli,
        [
            "web",
            "get",
            GET_LLMS_TXT_URL,
        ],
    )
    rtn = GetResult.model_validate(json.loads(result.output))
    llms_txt = rtn.get_context_by_type("llms_txt")
    assert llms_txt is not None
    assert "Send a structured list of input messages" in llms_txt.text
    assert len(llms_txt.text) < 400 * 1024
    assert result.exit_code == 0
    invalid_context = rtn.get_context_by_type("invalid")
    assert invalid_context is None


def test_web_cli_get_additional_context_llms_full_txt(runner) -> None:
    """Check getting additional context."""
    result = runner.invoke(
        cli,
        [
            "web",
            "get",
            "--llms-full-txt",
            GET_LLMS_TXT_URL,
        ],
    )
    rtn = GetResult.model_validate(json.loads(result.output))
    llms_txt = rtn.get_context_by_type("llms_txt")
    assert llms_txt is not None
    assert "knowledge base was last updated in August 2023" in llms_txt.text
    assert len(llms_txt.text) > 400 * 1024
    assert result.exit_code == 0


def test_web_cli_get_additional_context_not(runner) -> None:
    """Check not getting additional content."""
    result = runner.invoke(
        cli,
        [
            "web",
            "get",
            "--no-additional-context",
            GET_LLMS_TXT_URL,
        ],
    )
    rtn = GetResult.model_validate(json.loads(result.output))
    assert rtn.additional_context is None
    assert result.exit_code == 0
    llms_context = rtn.get_context_by_type("llms_txt")
    assert llms_context is None


def test_web_cli_get_forbidden_respected(runner) -> None:
    """Check getting content where robots.txt disallows fails."""
    result = runner.invoke(
        cli,
        [
            "web",
            "get",
            "https://github.com/search/advanced",
        ],
    )
    assert "robots.txt disallows crawling" in result.output
    assert result.exit_code == 1


def test_web_cli_get_forbidden_ignored(runner) -> None:
    """Check getting content where robots.txt disallows fails."""
    result = runner.invoke(
        cli,
        [
            "web",
            "get",
            "--force-not-respecting-robots-txt",
            "https://github.com/search/advanced",
        ],
    )
    assert "Where software is built" in result.output
    assert result.exit_code == 0
