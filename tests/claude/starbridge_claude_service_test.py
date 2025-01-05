"""Tests for Claude service functionality."""

from collections.abc import Generator
from unittest.mock import patch

import pytest

SUBPROCESS_RUN = "subprocess.run"


class TestClaudeService:
    """Test cases for the Claude service."""

    @pytest.fixture
    @staticmethod
    def mock_darwin() -> Generator[None, None, None]:
        """
        Mock platform.system to return Darwin.

        Yields:
            None: Yields control back after mocking.

        """
        with patch("platform.system", return_value="Darwin"):
            yield
