import json
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from starbridge.cli import cli
from starbridge.utils import Health


@pytest.fixture
def runner():
    return CliRunner()


@patch("starbridge.hello.service.Service.health")
def test_health_down(mock_health, runner):
    """Check health output when a service is down."""
    mock_health.return_value = Health(status=Health.Status.DOWN, reason="testing")
    result = runner.invoke(cli, ["health", "--json"])
    assert result.exit_code == 0

    # Clean up any whitespace/newlines before parsing
    health_data = json.loads(result.output.replace("\n", ""))
    assert "dependencies" in health_data
    assert health_data["dependencies"]["hello"]["status"] == "DOWN"
    assert health_data["dependencies"]["hello"]["reason"] == "testing"


@patch("starbridge.claude.service.Service.is_installed")
@patch("starbridge.claude.service.Service.is_running")
@patch("starbridge.confluence.service.Service.space_list")
def test_health_all_up(mock_space_list, mock_is_running, mock_is_installed, runner):
    """Check health when all services are up."""
    mock_is_installed.return_value = True
    mock_is_running.return_value = True
    mock_space_list.return_value = {"results": [{"name": "Test Space"}]}

    result = runner.invoke(cli, ["health", "--json"])
    assert result.exit_code == 0

    # Clean up any whitespace/newlines before parsing
    health_data = json.loads(result.output.replace("\n", ""))
    assert health_data["healthy"] is True
    assert "dependencies" in health_data

    # Verify each service status
    assert health_data["dependencies"]["claude"]["status"] == "UP"
    assert health_data["dependencies"]["confluence"]["status"] == "UP"
    assert health_data["dependencies"]["hello"]["status"] == "UP"

    # Verify no reasons for UP statuses
    for service in ["claude", "confluence", "hello"]:
        assert health_data["dependencies"][service].get("reason") is None
