import pytest
from pydantic import ValidationError

from starbridge.web import Resource


def test_web_types_resource_exactly_one():
    with pytest.raises(ValidationError):
        Resource(
            url="https://example.com", type="invalid", text="Hello World", blob=b"\0"
        )
    with pytest.raises(ValidationError):
        Resource(url="https://example.com", type="invalid", text=None, blob=None)
    Resource(url="https://example.com", type="invalid", text="Hello World", blob=None)
    Resource(url="https://example.com", type="invalid", text=None, blob=b"\0")
