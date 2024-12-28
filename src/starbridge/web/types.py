from enum import StrEnum


class Format(StrEnum):
    bytes = "bytes"
    unicode = "unicode"
    html = "html"
    markdown = "markdown"
    text = "text"


class RobotForbiddenException(Exception):
    pass
