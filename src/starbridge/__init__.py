"""⭐ Integrates Claude Desktop with the web, Google and Atlassian workspaces."""

import importlib.metadata
import os
import pathlib
import sys

__project_name__ = __name__.split(".")[0]
__project_path__ = str(pathlib.Path(__file__).parent.parent.parent)
__version__ = importlib.metadata.version(__project_name__)
__is_development_mode__ = "uvx" not in sys.argv[0].lower()
__is_running_in_container__ = os.getenv("STARBRIDGE_RUNNING_IN_CONTAINER") is not None


def _parse_env_args() -> None:
    """Parse --env arguments from command line and add to environment if STARBRIDGE_ prefixed."""
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if (args[i] == "--env" or args[i] == "-e") and i + 1 < len(args):
            try:
                key, value = args[i + 1].split("=", 1)
                if key.startswith("STARBRIDGE_"):
                    # Strip quotes if present
                    value = value.strip("\"'")
                    os.environ[key] = value
            except ValueError:
                pass  # Silently skip malformed env vars
        i += 1


def _amend_library_path() -> None:
    """Patch environment variables before any other imports."""
    if "DYLD_FALLBACK_LIBRARY_PATH" not in os.environ:
        os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = f"{os.getenv('HOMEBREW_PREFIX', '/opt/homebrew')}/lib/"


def _log_boot_message() -> None:
    # Local import as this initializes logging and instrumentation
    # which might depend on environment arguments parsed from argv
    from starbridge.utils import get_logger, get_process_info  # noqa: PLC0415

    logger = get_logger(__name__)

    process_info = get_process_info()
    logger.debug(
        "⭐ Booting Starbridge v%s (project root %s, pid %s), parent '%s' (pid %s)",
        __version__,
        process_info.project_root,
        process_info.pid,
        process_info.parent.name,
        process_info.parent.pid,
    )


# boot

_amend_library_path()
_parse_env_args()
_log_boot_message()

# exports

__all__ = [
    "__is_development_mode__",
    "__project_name__",
    "__project_path__",
    "__version__",
]
