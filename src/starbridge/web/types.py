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
