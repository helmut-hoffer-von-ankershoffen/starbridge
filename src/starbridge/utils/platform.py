import os
from pathlib import Path

import psutil
from pydantic import BaseModel


class ParentProcessInfo(BaseModel):
    name: str | None = None
    pid: int | None = None


class ProcessInfo(BaseModel):
    project_root: str
    pid: int
    parent: ParentProcessInfo


def get_process_info() -> ProcessInfo:
    """Get information about the current process and its parent."""
    current_process = psutil.Process()
    parent = current_process.parent()

    return ProcessInfo(
        project_root=str(Path(__file__).parent.parent.parent.parent),
        pid=current_process.pid,
        parent=ParentProcessInfo(
            name=parent.name() if parent else None, pid=parent.pid if parent else None
        ),
    )


def is_running_in_container() -> bool:
    return os.getenv("STARBRIDGE_RUNNING_IN_CONTAINER") is not None
