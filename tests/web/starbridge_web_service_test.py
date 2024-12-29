import asyncio

import pytest

from starbridge.web import RobotForbiddenException


def test_web_service_get_forbidden() -> None:
    """Check getting content from the web fails if forbidden by robots.txt."""

    from starbridge.web import Service

    with pytest.raises(RobotForbiddenException):
        asyncio.run(Service().get("https://github.com/search/advanced"))
