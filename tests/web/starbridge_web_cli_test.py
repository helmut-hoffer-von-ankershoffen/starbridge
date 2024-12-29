import json
from unittest.mock import patch

import pytest
import requests
from typer.testing import CliRunner

from starbridge.cli import cli

GET_TEST_URL = "https://helmuthva.gitbook.io/starbridge"
GET_LLMS_TXT_URL = "https://docs.anthropic.com"


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


def test_web_cli_get_html(runner):
    """Check getting content from the web as html encoded in unicode."""

    result = runner.invoke(
        cli,
        [
            "web",
            "get",
            "--no-transform-to-markdown",
            GET_TEST_URL,
        ],
    )
    assert json.loads(result.output)["resource"]["content"].startswith(
        "<!DOCTYPE html>"
    )
    assert result.exit_code == 0


def test_web_cli_get_markdown(runner):
    """Check getting content from the web as markdown."""

    result = runner.invoke(
        cli,
        [
            "web",
            "get",
            GET_TEST_URL,
        ],
    )
    assert "README | Starbridge" in json.loads(result.output)["resource"]["content"]
    assert result.exit_code == 0


def test_web_cli_get_french(runner):
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
    assert "Recherche" in json.loads(result.output)["resource"]["content"]
    assert result.exit_code == 0


def test_web_cli_get_additional_context_llms_text(runner):
    """Check getting additional context."""

    result = runner.invoke(
        cli,
        [
            "web",
            "get",
            GET_LLMS_TXT_URL,
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
            "--llms-full-txt",
            GET_LLMS_TXT_URL,
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
            "--no-additional-context",
            GET_LLMS_TXT_URL,
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
            GET_TEST_URL,
        ],
    )
    assert "Request failed" in result.output
    assert result.exit_code == 1
