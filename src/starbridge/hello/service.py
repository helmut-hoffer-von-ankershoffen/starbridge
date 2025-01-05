"""Handles Hello operations."""

import base64
import io
import os
from importlib.util import find_spec

from mcp.types import BlobResourceContents, EmbeddedResource
from pydantic import AnyUrl

from starbridge.mcp import MCPBaseService, MCPContext, mcp_tool
from starbridge.utils import Health, get_logger

logger = get_logger(__name__)


class Service(MCPBaseService):
    """Service class for Hello World operations."""

    @mcp_tool()
    def health(self, context: MCPContext | None = None) -> Health:  # noqa: ARG002, PLR6301
        """
        Check health of Hello World service.

        Args:
            context (MCPContext | None): Optional MCP context.

        Returns:
            Health: The health status of the service.

        """
        return Health(status=Health.Status.UP)

    @mcp_tool()
    def info(self, context: MCPContext | None = None) -> dict:  # noqa: ARG002, PLR6301
        """
        Info about Hello world environment.

        Args:
            context (MCPContext | None): Optional MCP context.

        Returns:
            dict: Information about the Hello World service environment.

        """
        return {"locale": "en_US"}

    @mcp_tool()
    def hello(self, locale: str = "en_US", context: MCPContext | None = None) -> str:  # noqa: ARG002, PLR6301
        """
        Print hello world in different languages.

        Args:
            locale (str): Language/region code to use for the greeting.
            context (MCPContext | None): Optional MCP context.

        Returns:
            str: The greeting message in the specified language.

        Raises:
            RuntimeError: If the service is configured to fail.

        """
        if "starbridge_hello_service_hello_fail" in os.environ.get("MOCKS", "").split(
            ",",
        ):
            msg = "Hello World failed"
            raise RuntimeError(msg)
        if locale == "de_DE":
            return "Hallo Welt!"
        return "Hello World!"

    if find_spec("cairosvg"):

        @mcp_tool()
        def bridge(self, context: MCPContext | None = None):  # noqa: ARG002, ANN201, PLR6301
            """
            Show image of starbridge.

            Args:
                context (MCPContext | None): Optional MCP context.

            Returns:
                PIL.Image.Image: Image object containing the starbridge logo

            """
            import cairosvg  # type: ignore # noqa: PLC0415
            from PIL import Image  # noqa: PLC0415

            return Image.open(
                io.BytesIO(
                    cairosvg.svg2png(bytestring=Service._starbridge_svg()) or b"",
                ),
            )

    @mcp_tool()
    def pdf(self, context: MCPContext | None = None) -> EmbeddedResource:  # noqa: ARG002, PLR6301
        """
        Show pdf document with Hello World.

        Args:
            context (MCPContext | None): Optional MCP context.

        Returns:
            EmbeddedResource: A PDF document containing Hello World

        """
        return EmbeddedResource(
            type="resource",
            resource=BlobResourceContents(
                uri=AnyUrl("starbridge://hello/pdf"),
                mimeType="application/pdf",
                blob=Service._starbridge_pdf_base64(),
            ),
        )

    @staticmethod
    def pdf_bytes(context: MCPContext | None = None) -> bytes:  # noqa: ARG004
        """
        Show pdf document with Hello World.

        Args:
            context (MCPContext | None): Optional MCP context.

        Returns:
            bytes: PDF document containing Hello World as bytes

        """
        return base64.b64decode(Service._starbridge_pdf_base64())

    @staticmethod
    def _starbridge_svg() -> str:
        """
        Image of starbridge, generated with Claude (Sonnet 3.5 new).

        Returns:
            str: SVG markup of the starbridge image

        """
        return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
    <!-- Background -->
    <rect width="256" height="256" fill="#1a1a2e"/>

    <!-- Stars in background -->
    <circle cx="30" cy="40" r="1" fill="white"/>
    <circle cx="80" cy="30" r="1.5" fill="white"/>
    <circle cx="150" cy="45" r="1" fill="white"/>
    <circle cx="200" cy="25" r="1.5" fill="white"/>
    <circle cx="220" cy="60" r="1" fill="white"/>
    <circle cx="50" cy="70" r="1" fill="white"/>
    <circle cx="180" cy="80" r="1.5" fill="white"/>

    <!-- Bridge structure -->
    <!-- Left support -->
    <path d="M40 180 L60 100 L80 180" fill="#4a4e69"/>
    <!-- Right support -->
    <path d="M176 180 L196 100 L216 180" fill="#4a4e69"/>

    <!-- Bridge deck -->
    <path d="M30 180 L226 180" stroke="#9a8c98" stroke-width="8" fill="none"/>

    <!-- Suspension cables -->
    <path d="M60 100 C128 50, 128 50, 196 100" stroke="#c9ada7" stroke-width="3" fill="none"/>
    <path d="M60 100 L80 180" stroke="#c9ada7" stroke-width="2" fill="none"/>
    <path d="M196 100 L176 180" stroke="#c9ada7" stroke-width="2" fill="none"/>

    <!-- Star decorations -->
    <path d="M128 70 L132 62 L140 60 L132 58 L128 50 L124 58 L116 60 L124 62 Z" fill="#ffd700"/>
    <path d="M60 95 L62 91 L66 90 L62 89 L60 85 L58 89 L54 90 L58 91 Z" fill="#ffd700"/>
    <path d="M196 95 L198 91 L202 90 L198 89 L196 85 L194 89 L190 90 L194 91 Z" fill="#ffd700"/>

    <!-- Reflection in water -->
    <path d="M40 180 L60 220 L80 180 M176 180 L196 220 L216 180" fill="#1a1a2e" opacity="0.3"/>
    <path d="M60 100 C128 150, 128 150, 196 100" stroke="#c9ada7" stroke-width="1" fill="none" opacity="0.2"/>
</svg>"""

    @staticmethod
    def _starbridge_pdf_base64() -> str:
        return "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IHRydWUgPj4gL1N0cnVjdFRyZWVSb290CjEwIDAgUiA+PgplbmRvYmoKNyAwIG9iagpbIDEgMCBSICAvWFlaIDAgODQxLjg5IDAgXQplbmRvYmoKNiAwIG9iago8PCAvVHlwZSAvRm9udCAvU3VidHlwZSAvVHJ1ZVR5cGUgL0Jhc2VGb250IC9BQUFBQUIrSGVsdmV0aWNhTmV1ZSAvRm9udERlc2NyaXB0b3IKMTMgMCBSIC9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZyAvRmlyc3RDaGFyIDMyIC9MYXN0Q2hhciAxMTQgL1dpZHRocyBbIDI3OAoyNTkgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwCjAgMCAwIDcyMiAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgOTI2IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDU5MyA1MzcKMCAwIDAgMCAwIDAgMjIyIDAgMCA1NzQgMCAwIDMzMyBdID4+CmVuZG9iagoxMyAwIG9iago8PCAvVHlwZSAvRm9udERlc2NyaXB0b3IgL0ZvbnROYW1lIC9BQUFBQUIrSGVsdmV0aWNhTmV1ZSAvRmxhZ3MgMzIgL0ZvbnRCQm94ClstOTUxIC00ODEgMTk4NyAxMDc3XSAvSXRhbGljQW5nbGUgMCAvQXNjZW50IDk1MiAvRGVzY2VudCAtMjEzIC9DYXBIZWlnaHQKNzE0IC9TdGVtViA5NSAvTGVhZGluZyAyOCAvWEhlaWdodCA1MTcgL1N0ZW1IIDgwIC9BdmdXaWR0aCA0NDcgL01heFdpZHRoIDIyMjUKL0ZvbnRGaWxlMiAxNCAwIFIgPj4KZW5kb2JqCjE0IDAgb2JqCjw8IC9MZW5ndGgxIDMzMjQgL0xlbmd0aCAxNzYyIC9GaWx0ZXIgL0ZsYXRlRGVjb2RlID4+CnN0cmVhbQp4Aa1XfWhbVRQ/974kbdP0I03Sj6Qf7zVZmjZpszZLatc2ptp0Tcfm3IfkdXS17eJaWe3QOuYfzoIfaBBRQWFDRBB1goxMZKYR3EDwWxh+IIwi/qOI+JdM/9G2/u57z9BucwzZS8+755x73rm/87v3naSLDz6cIRst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MjAwODE1NDhaMDAnMDAnKSAvTW9kRGF0ZSAoRDoyMDI0MTIyMDA4MTU0OFowMCcwMCcpCj4+CmVuZG9iagp4cmVmCjAgMTYKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwMjk2IDAwMDAwIG4gCjAwMDAwMDM0NTEgMDAwMDAgbiAKMDAwMDAwMDAyMiAwMDAwMCBuIAowMDAwMDAwNDA2IDAwMDAwIG4gCjAwMDAwMDMyMTUgMDAwMDAgbiAKMDAwMDAwMzY4NCAwMDAwMCBuIAowMDAwMDAzNjQyIDAwMDAwIG4gCjAwMDAwMDA1MDMgMDAwMDAgbiAKMDAwMDAwMzMwMyAwMDAwMCBuIAowMDAwMDAzMjUwIDAwMDAwIG4gCjAwMDAwMDMzODAgMDAwMDAgbiAKMDAwMDAwMzU0MCAwMDAwMCBuIAowMDAwMDA0MDQzIDAwMDAwIG4gCjAwMDAwMDQzMDkgMDAwMDAgbiAKMDAwMDAwNjE1OSAwMDAwMCBuIAp0cmFpbGVyCjw8IC9TaXplIDE2IC9Sb290IDEyIDAgUiAvSW5mbyAxNSAwIFIgL0lEIFsgPDgxZmRjNzY2OWY1ZmRkZmI1YWIwOTQ5ODdjNDU0ZDU1Pgo8ODFmZGM3NjY5ZjVmZGRmYjVhYjA5NDk4N2M0NTRkNTU+IF0gPj4Kc3RhcnR4cmVmCjYzNjIKJSVFT0YK"  # noqa: E501
