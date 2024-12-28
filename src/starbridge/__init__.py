import importlib.metadata
import os
import pathlib
import sys

# consts
__project_name__ = __name__.split(".")[0]
__project_path__ = str(pathlib.Path(__file__).parent.parent.parent)
__version__ = importlib.metadata.version(__project_name__)
__is_development_mode__ = "uvx" not in sys.argv[0].lower()

# helpers


def _parse_env_args():
    """Parse --env arguments from command line and add to environment if STARBRIDGE_ prefixed"""
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--env" and i + 1 < len(args):
            try:
                key, value = args[i + 1].split("=", 1)
                if key.startswith("STARBRIDGE_"):
                    # Strip quotes if present
                    value = value.strip("\"'")
                    os.environ[key] = value
            except ValueError:
                pass  # Silently skip malformed env vars
        i += 1


def _amend_library_path():
    """Patch environment variables before any other imports"""
    if "DYLD_FALLBACK_LIBRARY_PATH" not in os.environ:
        os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = (
            f"{os.getenv('HOMEBREW_PREFIX', '/opt/homebrew')}/lib/"
        )


def _log_boot_message():
    # Local import as this initializes logging and instrumentation
    # which might depend on environment arguments parsed from argv
    from starbridge.utils import get_logger, get_process_info

    logger = get_logger(__name__)

    process_info = get_process_info()
    logger.debug(
        f"⭐ Booting Starbridge v{__version__} (project root {process_info.project_root}, pid {process_info.pid}), parent '{process_info.parent.name}' (pid {process_info.parent.pid})"
    )


# boot

_amend_library_path()
_parse_env_args()
_log_boot_message()

# exports

__all__ = [
    "__version__",
    "__project_name__",
    "__project_path__",
    "__is_development_mode__",
]
