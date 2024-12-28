from enum import Enum


class Format(str, Enum):
    bytes = "bytes"
    unicode = "unicode"
    html = "html"
    markdown = "markdown"
    text = "text"


class RobotForbiddenException(Exception):
    pass
