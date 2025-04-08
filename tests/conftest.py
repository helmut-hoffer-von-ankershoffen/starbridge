"""Common test fixtures and configuration."""

import os
from pathlib import Path

import pytest


def pytest_collection_modifyitems(config, items) -> None:
    """Modify collected test items by skipping tests marked as 'long_running' unless matching marker given.

    Args:
        config: The pytest configuration object.
        items: The list of collected test items.
    """
    if not config.getoption("-m"):
        skip_me = pytest.mark.skip(reason="skipped as no marker given on execution using '-m'")
        for item in items:
            if "long_running" in item.keywords:
                item.add_marker(skip_me)


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig) -> str:
    """Get the path to the docker compose file.

    Args:
        pytestconfig: The pytest configuration object.

    Returns:
        str: The path to the docker compose file.
    """
    # We want to test the compose.yaml file in the root of the project.
    return str(Path(pytestconfig.rootdir) / "compose.yaml")


@pytest.fixture(scope="session")
def docker_setup() -> list[str] | str:
    """Commands to run when spinning up services.

    Args:
        scope: The scope of the fixture.

    Returns:
        list[str] | str: The commands to run.
    """
    # You can consider to return an empty list so you can decide on the
    # commands to run in the test itself
    return ["up --build -d"]


def docker_compose_project_name() -> str:
    """Generate a project name using the current process PID.

    Returns:
        str: The project name.
    """
    # You can consider to override this with a project name to reuse the stack
    # across test executions.
    return f"pytest{os.getpid()}"
