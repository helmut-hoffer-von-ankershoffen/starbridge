import json
from unittest.mock import patch

import pytest
import requests
from brave_search_python_client import WebSearchApiResponse
from typer.testing import CliRunner

from starbridge.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_search_cli_info(runner):
    """Check search info."""

    result = runner.invoke(cli, ["search", "info"])
    assert result.exit_code == 0


def test_search_cli_health(runner):
    """Check search health."""

    result = runner.invoke(cli, ["search", "health"])
    assert '"UP"' in result.output
    assert result.exit_code == 0


@patch("requests.head")
def test_search_cli_health_not_connected(mock_head, runner):
    """Check web health down when not connected."""
    mock_head.side_effect = requests.exceptions.Timeout()

    result = runner.invoke(cli, ["search", "health"])
    assert '"DOWN"' in result.output
    assert result.exit_code == 0


def test_search_cli_web(runner):
    """Check searching the web."""

    result = runner.invoke(
        cli,
        [
            "search",
            "web",
            "hello world",
        ],
    )
    assert result.exit_code == 0
    _response = WebSearchApiResponse.model_validate(json.loads(result.output))
    assert _response.web and _response.web.results and len(_response.web.results) > 0


@patch("httpx.AsyncClient.get")
def test_search_cli_get_timeouts(mock_get, runner):
    """Check getting content fails."""
    mock_get.side_effect = requests.exceptions.Timeout()

    result = runner.invoke(
        cli,
        [
            "search",
            "web",
            "hello world",
        ],
    )
    assert "Request failed" in result.output
    assert result.exit_code == 1
