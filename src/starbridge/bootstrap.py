import os
import sys

from starbridge.base import __version__
from starbridge.utils import get_logger, get_process_info


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


# Execute immediately when this module is imported
_parse_env_args()
_amend_library_path()

# Initializes logging and instrumentation
logger = get_logger(__name__)

process_info = get_process_info()
logger.debug(
    f"⭐ Booting Starbridge v{__version__} (project root {process_info.project_root}, pid {process_info.pid}), parent '{process_info.parent.name}' (pid {process_info.parent.pid})"
)
