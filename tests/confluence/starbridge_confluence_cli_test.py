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
FIXTURE_GET_ALL_SPACES = "tests/fixtures/get_all_spaces.json"


@pytest.fixture
def runner():
    return CliRunner()


@patch(MOCK_GET_ALL_SPACES)
def test_confluence_health(mock_get_all_spaces, runner):
    """Check health."""
    # Mock the response data that would come from get_all_spaces
    with Path(FIXTURE_GET_ALL_SPACES).open() as f:
        mock_get_all_spaces.return_value = json.loads(f.read())

    result = runner.invoke(cli, ["confluence", "health"])
    assert '"UP"' in result.output
    assert result.exit_code == 0


def test_confluence_info(runner):
    """Check info."""
    result = runner.invoke(cli, ["confluence", "info"])
    assert result.exit_code == 0


@patch(MOCK_GET_ALL_SPACES)
def test_confluence_mcp_resources(mock_get_all_spaces, runner):
    """Check fetching resources."""
    # Mock the response data that would come from get_all_spaces
    with Path(FIXTURE_GET_ALL_SPACES).open() as f:
        mock_get_all_spaces.return_value = json.loads(f.read())

    result = runner.invoke(cli, ["confluence", "mcp", "resources"])
    assert "helmut" in result.output
    assert result.exit_code == 0


def test_confluence_mcp_resource_types(runner):
    """Check resource types including space."""
    result = runner.invoke(cli, ["confluence", "mcp", "resource-types"])
    assert "space" in result.output
    assert result.exit_code == 0


@patch(MOCK_GET_SPACE)
def test_confluence_mcp_space(mock_get_space, runner):
    """Check getting space."""
    # Mock the response data that would come from get_all_spaces
    with Path("tests/fixtures/get_space.json").open() as f:
        mock_get_space.return_value = json.loads(f.read())

    result = runner.invoke(
        cli, ["confluence", "mcp", "space", "~7120201709026d2b41448e93bb58d5fa301026"]
    )
    assert "helmut" in result.output
    assert result.exit_code == 0


def test_confluence_mcp_prompts(runner):
    """Check prompts."""
    result = runner.invoke(cli, ["confluence", "mcp", "prompts"])
    assert "summary" in result.output
    assert result.exit_code == 0


@patch(MOCK_GET_ALL_SPACES)
def test_confluence_mcp_space_summary(mock_get_all_spaces, runner):
    """Check space list."""
    # Mock the response data that would come from get_all_spaces
    with Path(FIXTURE_GET_ALL_SPACES).open() as f:
        mock_get_all_spaces.return_value = json.loads(f.read())

    result = runner.invoke(
        cli, ["confluence", "mcp", "space-summary", "--style", "detailed"]
    )
    assert "helmut" in result.output
    assert result.exit_code == 0


@patch(MOCK_GET_ALL_SPACES)
def test_confluence_space_list(mock_get_all_spaces, runner):
    """Check space list."""
    # Mock the response data that would come from get_all_spaces
    with Path(FIXTURE_GET_ALL_SPACES).open() as f:
        mock_get_all_spaces.return_value = json.loads(f.read())

    result = runner.invoke(cli, ["confluence", "space", "list"])
    assert "helmut" in result.output
    assert result.exit_code == 0


@patch(MOCK_GET_PAGE_BY_ID)
def test_confluence_page_read(get_page_by_id, runner):
    """Check page list."""
    # Mock the response data that would come from get_all_spaces
    with Path("tests/fixtures/get_page_by_id.json").open() as f:
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


@patch(MOCK_GET_ALL_PAGES_FROM_SPACE)
def test_confluence_page_list(mock_get_all_pages_from_space, runner):
    """Check page list."""
    # Mock the response data that would come from get_all_spaces
    with Path("tests/fixtures/get_all_pages_from_space.json").open() as f:
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


def test_mcp_tools(runner):
    """Check tools include listing spaces and creating pages."""
    result = runner.invoke(cli, ["confluence", "mcp", "tools"])
    assert result.exit_code == 0
    assert "name='starbridge_confluence_info'" in result.stdout
    assert "name='starbridge_confluence_page_create'" in result.stdout
    assert "name='starbridge_confluence_space_list'" in result.stdout
