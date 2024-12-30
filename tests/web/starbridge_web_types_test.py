import pytest
from pydantic import AnyHttpUrl, ValidationError

from starbridge.web import Resource

EXAMPLE_COM = "https://example.com"


def test_web_types_resource_exactly_one():
    with pytest.raises(ValidationError):
        Resource(
            url=AnyHttpUrl(EXAMPLE_COM),
            type="invalid",
            text="Hello World",
            blob=b"\0",
        )
    with pytest.raises(ValidationError):
        Resource(url=AnyHttpUrl(EXAMPLE_COM), type="invalid", text=None, blob=None)
    Resource(
        url=AnyHttpUrl(EXAMPLE_COM),
        type="invalid",
        text="Hello World",
        blob=None,
    )
    Resource(url=AnyHttpUrl(EXAMPLE_COM), type="invalid", text=None, blob=b"\0")
