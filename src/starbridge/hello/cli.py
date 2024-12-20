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

from starbridge.utils.console import console

from .service import Service

cli = typer.Typer(no_args_is_help=True)


@cli.command()
def health():
    """Health of Hello World"""
    console.print(Service().health())


@cli.command()
def info():
    """Info about Hello World"""
    console.print(Service().info())


@cli.command()
def hello():
    """Print Hello World!"""
    console.print(Service().hello())


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
    image = Service().bridge()
    if dump:
        image.save("starbridge.png")
    else:
        image.show()


@cli.command()
def pdf(
    dump: Annotated[
        bool,
        typer.Option(
            help="If set, will dump to file starbridge.pdf in current working directory. Defaults to opening viewer to show the document."
        ),
    ] = False,
) -> None:
    """Show image of starbridge"""
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
