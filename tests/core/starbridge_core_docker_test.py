"""Test docker functionality of the Starbridge core package."""

import pytest
import requests
from requests.exceptions import ConnectionError as RequestsConnectionError


def is_responsive(url) -> bool | None:
    """
    Check if a given URL is responsive.

    Args:
        url: The URL to check

    Returns:
        bool: True if URL is responsive, False if not responsive
        None: If connection failed

    """
    try:
        response = requests.get(url, timeout=5.0)
        if response.status_code == 200:
            return True
    except RequestsConnectionError:
        return False


@pytest.fixture(scope="session")
def inspector_service(docker_ip, docker_services) -> str:
    """Ensure that HTTP service is up and responsive."""
    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("starbridge_inspector", 5173)
    url = f"http://{docker_ip}:{port}"
    docker_services.wait_until_responsive(
        timeout=5.0,
        pause=0.1,
        check=lambda: is_responsive(url),
    )
    return url


@pytest.mark.xdist_group(name="docker")
@pytest.mark.skip_with_act
def test_core_docker_inspector_healthy(inspector_service) -> None:
    """Test that the docker inspector service is healthy and responding."""
    status = 200
    response = requests.get(inspector_service + "/", timeout=5.0)

    assert response.status_code == status
    assert "mcp.svg" in response.content.decode("utf-8")


@pytest.mark.xdist_group(name="docker")
@pytest.mark.skip_with_act
def test_core_docker_cli_help_with_love(docker_services) -> None:
    """Test the CLI help command with docker services returns expected output."""
    out = docker_services._docker_compose.execute("run starbridge --help ")
    out_str = out.decode("utf-8")
    assert "built with love in Berlin" in out_str


@pytest.mark.xdist_group(name="docker")
@pytest.mark.skip_with_act
def test_core_docker_cli_mcp_services(docker_services) -> None:
    """Test the MCP services command with docker services returns expected output."""
    out = docker_services._docker_compose.execute("run starbridge mcp services")
    out_str = out.decode("utf-8")
    assert "claude" in out_str
    assert "confluence" in out_str
    assert "hello" in out_str
