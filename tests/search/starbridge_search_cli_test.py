"""Test search CLI functionality."""

import json
from unittest.mock import patch

import httpx
import pytest
import requests
from brave_search_python_client import MOCK_API_KEY, WebSearchApiResponse
from typer.testing import CliRunner

from starbridge.cli import cli


@pytest.fixture
def runner() -> CliRunner:
    """Get a Click CLI test runner."""
    return CliRunner()


def test_search_cli_info(runner) -> None:
    """Check search info."""
    result = runner.invoke(cli, ["search", "info"])
    assert result.exit_code == 0


def test_search_cli_health(runner) -> None:
    """Check search health."""
    result = runner.invoke(cli, ["search", "health"])
    assert '"UP"' in result.output
    assert result.exit_code == 0


@patch("httpx.AsyncClient.head")
def test_search_cli_health_not_connected(mock_head, runner) -> None:
    """Check web health down when not connected."""
    mock_head.side_effect = httpx.ReadTimeout("Timeout")

    result = runner.invoke(cli, ["search", "health"])
    assert '"DOWN"' in result.output
    assert result.exit_code == 0


def test_search_cli_web(runner) -> None:
    """Check searching the web."""
    with patch.dict(
        "os.environ",
        {"STARBRIDGE_SEARCH_BRAVE_SEARCH_API_KEY": MOCK_API_KEY},
    ):
        result = runner.invoke(
            cli,
            [
                "search",
                "web",
                "hello world",
            ],
        )
        assert result.exit_code == 0
        response = WebSearchApiResponse.model_validate(json.loads(result.output))
        assert response.web
        assert response.web.results
        assert len(response.web.results) > 0


@patch("httpx.AsyncClient.get")
def test_search_cli_get_timeouts(mock_get, runner) -> None:
    """Check getting content fails."""
    mock_get.side_effect = requests.exceptions.Timeout()

    with patch.dict("os.environ", {"STARBRIDGE_SEARCH_BRAVE_SEARCH_API_KEY": "OTHER"}):
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
