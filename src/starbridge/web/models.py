"""Data type definitions for web interactions."""

from typing import Annotated

from pydantic import AnyHttpUrl, AnyUrl, BaseModel, Field, model_validator


class RobotForbiddenError(Exception):
    """Exception raised when access to a URL is forbidden by robots.txt."""


class MimeType:
    """Constants for commonly used MIME types in web interactions."""

    TEXT_HTML = "text/html"
    TEXT_MARKDWON = "text/markdown"
    TEXT_PLAIN = "text/plain"
    APPLICATION_PDF = "application/pdf"
    APPLICATION_OPENXML_WORD = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    APPLICATION_OPENXML_EXCEL = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    OCTET_STREAM = "application/octet-stream"


HTML_PARSER = "html.parser"


class Resource(BaseModel):
    """A model representing a web resource with its URL, type, and content (text or binary)."""

    url: Annotated[AnyHttpUrl, Field(description="Final URL of the resource")]
    type: Annotated[str, Field(description="MIME type of the resource", min_length=4)]
    text: Annotated[
        str | None,
        Field(
            description="Textual content of the resource. None if the resource is binary.",
        ),
    ] = None
    blob: Annotated[
        bytes | None,
        Field(
            description="Binary content of the resource. None if the resource has textual content.",
        ),
    ] = None

    @model_validator(mode="after")
    def check_content_exists(self) -> "Resource":
        """
        Validate that either text or blob content exists, but not both.

        Returns:
            Resource: The validated resource instance

        Raises:
            ValueError: If neither text nor blob is provided, or if both are provided

        """
        if self.text is None and self.blob is None:
            msg = "Either text or blob must be provided"
            raise ValueError(msg)
        if self.text is not None and self.blob is not None:
            msg = "Only one of text or blob must be provided"
            raise ValueError(msg)
        return self


class LinkTarget(BaseModel):
    """A model representing a link target in a web resource with its URL, occurrences and anchor texts."""

    url: Annotated[AnyUrl, Field(description="URL of the link target")]
    occurrences: Annotated[
        int,
        Field(
            description="Number of occurrences of the url as a link target in the resource",
            ge=0,
        ),
    ]

    anchor_texts: Annotated[
        list[str],
        Field(description="Anchor texts of the link target", min_length=1),
    ]


class Context(BaseModel):
    """A model representing additional context information about a web resource or its domain."""

    type: Annotated[str, Field(description="Type of context")]
    url: Annotated[AnyHttpUrl, Field(description="URL of the context")]
    text: Annotated[str, Field(description="Content of context in markdown format")]


class GetResult(BaseModel):
    """
    A model representing the result of a web resource fetch operation.

    Includes the resource, extracted links, and additional context.
    """

    def get_context_by_type(self, context_type: str) -> Context | None:
        """
        Get text of additional context of given type.

        Args:
            context_type: The type of context to retrieve

        Returns:
            Context | None: The context of the specified type, or None if not found

        """
        if not self.additional_context:
            return None
        for ctx in self.additional_context:
            if ctx.type == context_type:
                return ctx
        return None

    def get_link_count(self) -> int:
        """
        Get number of extracted links.

        Returns:
            int: The number of extracted links

        """
        return len(self.extracted_links or [])

    resource: Annotated[
        Resource,
        Field(description="The retrieved and possibly transformed resource"),
    ]
    extracted_links: Annotated[
        list[LinkTarget] | None,
        Field(
            default=None,
            description="List of link targets extracted from the resource, if extract_links=True. "
            "Sorted by number of occurrences of a URL in the resource",
        ),
    ] = None
    additional_context: Annotated[
        list[Context] | None,
        Field(
            default=None,
            description="List of additional context about the URL or it's domain in the response",
        ),
    ] = None
