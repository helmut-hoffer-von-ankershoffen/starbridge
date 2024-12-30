from unittest.mock import patch

from starbridge.utils import is_running_in_container


def test_container_running_in_platform():
    """Check behavior of container running in platform."""

    assert is_running_in_container() is False

    def mock_getenv(key, default=None):
        if key == "STARBRIDGE_RUNNING_IN_CONTAINER":
            return "True"
        return None

    with patch("os.getenv", side_effect=mock_getenv):
        assert is_running_in_container() is True
