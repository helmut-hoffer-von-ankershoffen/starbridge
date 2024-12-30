from unittest.mock import patch

import pytest

SUBPROCESS_RUN = "subprocess.run"


class TestClaudeService:
    @pytest.fixture
    def mock_darwin(self):
        with patch("platform.system", return_value="Darwin"):
            yield
