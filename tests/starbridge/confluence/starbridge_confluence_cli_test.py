"""Tests for Confluence CLI functionality."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from starbridge.cli import cli

MOCK_GET_ALL_SPACES = "atlassian.Confluence.get_all_spaces"
MOCK_GET_SPACE = "atlassian.Confluence.get_space"
MOCK_GET_ALL_PAGES_FROM_SPACE = "atlassian.Confluence.get_all_pages_from_space"
MOCK_GET_PAGE_BY_ID = "atlassian.Confluence.get_page_by_id"
MOCK_CQL = "atlassian.Confluence.cql"
FIXTURE_GET_ALL_SPACES = "tests/fixtures/get_all_spaces.json"


@pytest.fixture
def runner() -> CliRunner:
    """Get a Click CLI test runner."""
    return CliRunner()


@patch(MOCK_GET_ALL_SPACES)
def test_confluence_cli_health(mock_get_all_spaces, runner) -> None:
    """Check health."""
    # Mock the response data that would come from get_all_spaces
    with Path(FIXTURE_GET_ALL_SPACES).open(encoding="utf-8") as f:
        mock_get_all_spaces.return_value = json.loads(f.read())

    result = runner.invoke(cli, ["confluence", "health"])
    assert '"UP"' in result.output
    assert result.exit_code == 0


def test_confluence_cli_info(runner) -> None:
    """Check info."""
    result = runner.invoke(cli, ["confluence", "info"])
    assert result.exit_code == 0


@patch(MOCK_GET_ALL_SPACES)
def test_confluence_cli_mcp_resources(mock_get_all_spaces, runner) -> None:
    """Check fetching resources."""
    # Mock the response data that would come from get_all_spaces
    with Path(FIXTURE_GET_ALL_SPACES).open(encoding="utf-8") as f:
        mock_get_all_spaces.return_value = json.loads(f.read())

    result = runner.invoke(cli, ["confluence", "mcp", "resources"])
    assert "helmut" in result.output
    assert result.exit_code == 0


def test_confluence_mcp_resource_types(runner) -> None:
    """Check resource types including space."""
    result = runner.invoke(cli, ["confluence", "mcp", "resource-types"])
    assert "space" in result.output
    assert result.exit_code == 0


@patch(MOCK_GET_SPACE)
def test_confluence_cli_mcp_space(mock_get_space, runner) -> None:
    """Check getting space."""
    # Mock the response data that would come from get_all_spaces
    with Path("tests/fixtures/get_space.json").open(encoding="utf-8") as f:
        mock_get_space.return_value = json.loads(f.read())

    result = runner.invoke(
        cli,
        ["confluence", "mcp", "space", "~7120201709026d2b41448e93bb58d5fa301026"],
    )
    assert "helmut" in result.output
    assert result.exit_code == 0


def test_confluence_cli_mcp_prompts(runner) -> None:
    """Check prompts."""
    result = runner.invoke(cli, ["confluence", "mcp", "prompts"])
    assert "summary" in result.output
    assert result.exit_code == 0


@patch(MOCK_GET_ALL_SPACES)
def test_confluence_cli_mcp_space_summary(mock_get_all_spaces, runner) -> None:
    """Check space list."""
    # Mock the response data that would come from get_all_spaces
    with Path(FIXTURE_GET_ALL_SPACES).open(encoding="utf-8") as f:
        mock_get_all_spaces.return_value = json.loads(f.read())

    result = runner.invoke(
        cli,
        ["confluence", "mcp", "space-summary", "--style", "detailed"],
    )
    assert "helmut" in result.output
    assert result.exit_code == 0


def test_confluence_cli_mcp_tools(runner) -> None:
    """Check tools include listing spaces and creating pages."""
    result = runner.invoke(cli, ["confluence", "mcp", "tools"])
    assert result.exit_code == 0
    assert "name='starbridge_confluence_info'" in result.stdout
    assert "name='starbridge_confluence_page_create'" in result.stdout
    assert "name='starbridge_confluence_space_list'" in result.stdout


@patch(MOCK_GET_ALL_SPACES)
def test_confluence_space_list(mock_get_all_spaces, runner) -> None:
    """Check space list."""
    # Mock the response data that would come from get_all_spaces
    with Path(FIXTURE_GET_ALL_SPACES).open(encoding="utf-8") as f:
        mock_get_all_spaces.return_value = json.loads(f.read())

    result = runner.invoke(cli, ["confluence", "space", "list"])
    assert "helmut" in result.output
    assert result.exit_code == 0


@patch(MOCK_GET_PAGE_BY_ID)
def test_confluence_cli_page_read(get_page_by_id, runner) -> None:
    """Check page list."""
    # Mock the response data that would come from get_all_spaces
    with Path("tests/fixtures/get_page_by_id.json").open(encoding="utf-8") as f:
        get_page_by_id.return_value = json.loads(f.read())
    result = runner.invoke(
        cli,
        [
            "confluence",
            "page",
            "read",
            "--page-id",
            '"2088927594"',
        ],
    )
    assert "Amazon Leadership Principles" in result.output
    assert result.exit_code == 0


@patch(MOCK_CQL)
def test_confluence_cli_page_search(cql, runner) -> None:
    """Check page list."""
    # Mock the response data that would come from get_all_spaces
    with Path("tests/fixtures/confluence_page_search.json").open(encoding="utf-8") as f:
        cql.return_value = json.loads(f.read())
    result = runner.invoke(
        cli,
        [
            "confluence",
            "page",
            "search",
            "--query",
            '"title ~ Helmut"',
        ],
    )
    assert "4711" in result.output
    assert result.exit_code == 0


@patch(MOCK_GET_ALL_PAGES_FROM_SPACE)
def test_confluence_cli_page_list(mock_get_all_pages_from_space, runner) -> None:
    """Check page list."""
    # Mock the response data that would come from get_all_spaces
    with Path("tests/fixtures/get_all_pages_from_space.json").open(encoding="utf-8") as f:
        mock_get_all_pages_from_space.return_value = json.loads(f.read())
    result = runner.invoke(
        cli,
        [
            "confluence",
            "page",
            "list",
            "--space-key",
            '"~7120201709026d2b41448e93bb58d5fa301026"',
        ],
    )
    assert "Amazon Leadership Principles" in result.output
    assert result.exit_code == 0
