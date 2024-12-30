from typing import Annotated

from pydantic import BaseModel, Field


class RobotForbiddenException(Exception):
    pass


class MimeType:
    TEXT_HTML = "text/html"
    TEXT_MARKDWON = "text/markdown"
    TEXT_PLAIN = "text/plain"
    APPLICATION_PDF = "application/pdf"
    APPLICATION_OPENXML_WORD = (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    APPLICATION_OPENXML_EXCEL = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    OCTET_STREAM = "application/octet-stream"


HTML_PARSER = "html.parser"


class Resource(BaseModel):
    url: Annotated[str, Field(description="Final URL of the resource")]
    type: Annotated[str, Field(description="MIME type of the resource")]
    text: Annotated[
        str | None,
        Field(
            description="Textual content of the resource. None if the resource is binary."
        ),
    ] = None
    blob: Annotated[
        bytes | None,
        Field(
            description="Binary content of the resource. None if the resource has textual content."
        ),
    ] = None


class LinkTarget(BaseModel):
    url: Annotated[str, Field(description="URL of the link target")]
    occurences: Annotated[
        int,
        Field(
            description="Number of occurences of the url as a link target in the resource"
        ),
    ]
    anchor_texts: Annotated[
        list[str],
        Field(description="Anchor texts of the link target"),
    ]


class Context(BaseModel):
    type: Annotated[str, Field(description="Type of context")]
    url: Annotated[str, Field(description="URL of the context")]
    text: Annotated[str, Field(description="Content of context in markdown format")]


class GetResult(BaseModel):
    def get_context_by_type(self, context_type: str) -> Context | None:
        """Get text of additional context of given type."""
        if not self.additional_context:
            return None
        for ctx in self.additional_context:
            if ctx.type == context_type:
                return ctx
        return None

    def get_link_count(self) -> int:
        """Get number of extracted links."""
        return len(self.extracted_links or [])

    resource: Annotated[
        Resource, Field(description="The retrieved and possibly transformed resource")
    ]
    extracted_links: Annotated[
        list[LinkTarget] | None,
        Field(
            default=None,
            description="List of link targets extracted from the resource, if extract_links=True. Sorted by number of occurrences of a URL in the resource",
        ),
    ] = None
    additional_context: Annotated[
        list[Context] | None,
        Field(
            default=None,
            description="List of additional context about the URL or it's domain in the response",
        ),
    ] = None
