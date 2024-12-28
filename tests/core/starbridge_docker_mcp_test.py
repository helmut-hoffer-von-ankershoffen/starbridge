import pytest
import requests
from requests.exceptions import ConnectionError


def is_responsive(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False


@pytest.fixture(scope="session")
def inspector_service(docker_ip, docker_services):
    """Ensure that HTTP service is up and responsive."""

    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("starbridge_inspector", 5173)
    url = f"http://{docker_ip}:{port}"
    docker_services.wait_until_responsive(
        timeout=5.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return url


@pytest.mark.xdist_group(name="docker")
def test_starbridge_docker_inspector_healthy(inspector_service):
    status = 200
    response = requests.get(inspector_service + "/")

    assert response.status_code == status
    assert "mcp.svg" in response.content.decode("utf-8")


@pytest.mark.xdist_group(name="docker")
def test_starbridge_docker_cli_help_with_love(docker_services):
    out = docker_services._docker_compose.execute("run starbridge --help ")
    out_str = out.decode("utf-8")
    assert "built with love in Berlin" in out_str


@pytest.mark.xdist_group(name="docker")
def test_starbridge_docker_cli_mcp_services(docker_services):
    out = docker_services._docker_compose.execute("run starbridge mcp services")
    out_str = out.decode("utf-8")
    assert "claude" in out_str
    assert "confluence" in out_str
    assert "hello" in out_str
