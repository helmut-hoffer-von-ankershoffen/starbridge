"""
CLI to interact with Hello World
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Annotated

import typer
from rich.panel import Panel
from rich.text import Text

from starbridge.utils.console import console

from .service import Service

cli = typer.Typer(name="hello", help="Hello operations")


@cli.command()
def health():
    """Health of Hello World"""
    console.print_json(Service().health().model_dump_json())


@cli.command()
def info():
    """Info about Hello World"""
    console.print(Service().info())


@cli.command()
def hello(locale: Annotated[str, typer.Option(help="Locale to use")] = "en_US") -> None:
    """Print Hello World!"""
    console.print(Service().hello(locale))


if hasattr(Service, "bridge"):

    @cli.command()
    def bridge(
        dump: Annotated[
            bool,
            typer.Option(
                help="If set, will dump to file starbridge.png in current working directory. Defaults to opening viewer to show the image."
            ),
        ] = False,
    ) -> None:
        """Show image of starbridge"""
        try:
            image = Service().bridge()
            if dump:
                image.save("starbridge.png")
            else:
                image.show()
        except OSError:
            text = Text()
            text.append("Please follow setup instructions for starbridge ")
            text.append("Install the library needed for image manipulation using:\n")
            text.append("• macOS: ", style="yellow")
            text.append("brew install cairo\n")
            text.append("• Linux: ", style="yellow")
            text.append("sudo apt-get install libcairo2")
            console.print(
                Panel(
                    text,
                    title="Setup Required: Cairo not found",
                    border_style="red",
                )
            )
            sys.exit(78)


@cli.command()
def pdf(
    dump: Annotated[
        bool,
        typer.Option(
            help="If set, will dump to file starbridge.pdf in current working directory. Defaults to opening viewer to show the document."
        ),
    ] = False,
) -> None:
    """Show pdf of starbridge"""
    pdf = Service().pdf_bytes()

    if dump:
        pdf_path = Path("starbridge.pdf")
        pdf_path.write_bytes(pdf)
    else:
        # Create temporary file that gets auto-deleted when closed
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(pdf)
            tmp_path = Path(tmp.name)
            try:
                if sys.platform == "darwin":  # macOS
                    subprocess.run(["open", tmp_path], check=True)
                elif sys.platform == "win32":  # Windows
                    os.startfile(tmp_path)  # type: ignore
                else:  # Linux and others
                    subprocess.run(["xdg-open", tmp_path], check=True)

                # Give the viewer some time to open the file
                import time

                time.sleep(2)
            finally:
                # Clean up temp file after viewer has opened it
                tmp_path.unlink(missing_ok=True)
