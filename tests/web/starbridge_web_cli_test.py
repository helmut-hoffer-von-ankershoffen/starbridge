import json
from unittest.mock import patch

import pytest
import requests
from typer.testing import CliRunner

from starbridge.cli import cli

GET_TEST_URL = "https://helmuthva.gitbook.io/starbridge"


@pytest.fixture
def runner():
    return CliRunner()


def test_web_cli_info(runner):
    """Check web info."""

    result = runner.invoke(cli, ["web", "info"])
    assert result.exit_code == 0


def test_web_cli_health(runner):
    """Check web health."""

    result = runner.invoke(cli, ["web", "health"])
    assert '"UP"' in result.output
    assert result.exit_code == 0


@patch("requests.head")
def test_web_cli_health_not_connected(mock_head, runner):
    """Check web health down when not connected."""
    mock_head.side_effect = requests.exceptions.Timeout()

    result = runner.invoke(cli, ["web", "health"])
    assert '"DOWN"' in result.output
    assert result.exit_code == 0


def test_web_cli_get_bytes(runner):
    """Check getting content from the web as raw bytes."""

    result = runner.invoke(
        cli,
        [
            "web",
            "get",
            "--format",
            "bytes",
            GET_TEST_URL,
        ],
    )
    assert "b'<!DOCTYPE html>" in result.output
    assert result.exit_code == 0


def test_web_cli_get_unicode(runner):
    """Check getting content from the web as unicode encoded text."""

    result = runner.invoke(
        cli,
        [
            "web",
            "get",
            "--format",
            "unicode",
            GET_TEST_URL,
        ],
    )
    assert json.loads(result.output)["content"].startswith("<!DOCTYPE html>")
    assert result.exit_code == 0


def test_web_cli_get_html(runner):
    """Check getting content from the web as html encoded in unicode."""

    result = runner.invoke(
        cli,
        [
            "web",
            "get",
            "--format",
            "html",
            GET_TEST_URL,
        ],
    )
    assert json.loads(result.output)["content"].startswith("<!DOCTYPE html>")
    assert result.exit_code == 0


def test_web_cli_get_markdown(runner):
    """Check getting content from the web as markdown."""

    result = runner.invoke(
        cli,
        [
            "web",
            "get",
            "--format",
            "markdown",
            GET_TEST_URL,
        ],
    )
    assert (
        "Starbridge[![](https://helmuthva.gitbook.io"
        in json.loads(result.output)["content"]
    )
    assert result.exit_code == 0


def test_web_cli_get_text(runner):
    """Check getting content from the web as plain text."""

    result = runner.invoke(
        cli,
        [
            "web",
            "get",
            "--format",
            "text",
            GET_TEST_URL,
        ],
    )
    assert json.loads(result.output)["content"].startswith("README | Starbridge")
    assert result.exit_code == 0


def test_web_cli_get_french(runner):
    """Check getting content from the web in french."""

    result = runner.invoke(
        cli,
        [
            "web",
            "get",
            "--format",
            "text",
            "--accept-language",
            "fr_FR",
            "https://www.google.com",
        ],
    )
    assert "Recherche" in json.loads(result.output)["content"]
    assert result.exit_code == 0


def test_web_cli_get_additional_context_llms_text(runner):
    """Check getting additional context."""

    result = runner.invoke(
        cli,
        [
            "web",
            "get",
            "--format",
            "text",
            "https://docs.anthropic.com/",
        ],
    )
    assert "Get Api Key" in json.loads(result.output)["context"]["llms_txt"]
    assert len(json.loads(result.output)["context"]["llms_txt"]) < 400 * 1024
    assert result.exit_code == 0


def test_web_cli_get_additional_context_llms_full_txt(runner):
    """Check getting additional context."""

    result = runner.invoke(
        cli,
        [
            "web",
            "get",
            "--format",
            "text",
            "--llms-full-txt",
            "https://docs.anthropic.com/",
        ],
    )
    assert "Get Api Key" in json.loads(result.output)["context"]["llms_txt"]
    assert len(json.loads(result.output)["context"]["llms_txt"]) > 400 * 1024
    assert result.exit_code == 0


def test_web_cli_get_additional_context_not(runner):
    """Check not getting additional content."""

    result = runner.invoke(
        cli,
        [
            "web",
            "get",
            "--format",
            "text",
            "--no-additional-context",
            "https://docs.anthropic.com/",
        ],
    )
    assert hasattr(json.loads(result.output), "context") is False
    assert result.exit_code == 0


def test_web_cli_get_forbidden(runner):
    """Check getting content where robots.txt disallows fails."""

    result = runner.invoke(
        cli,
        [
            "web",
            "get",
            "--format",
            "text",
            "https://github.com/search/advanced",
        ],
    )
    assert "robots.txt disallows crawling" in result.output
    assert result.exit_code == 1


@patch("httpx.AsyncClient.get")
def test_web_cli_get_timeouts(mock_get, runner):
    """Check getting content fails."""
    mock_get.side_effect = requests.exceptions.Timeout()

    result = runner.invoke(
        cli,
        [
            "web",
            "get",
            "--format",
            "bytes",
            GET_TEST_URL,
        ],
    )
    assert "Request failed" in result.output
    assert result.exit_code == 1
