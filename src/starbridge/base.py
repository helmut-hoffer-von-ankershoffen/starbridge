import importlib.metadata
import pathlib
import sys

__project_name__ = __name__.split(".")[0]
__project_path__ = str(pathlib.Path(__file__).parent.parent.parent)
__version__ = importlib.metadata.version(__project_name__)
__is_development_mode__ = "uvx" not in sys.argv[0].lower()


__all__ = [
    "__version__",
    "__project_name__",
    "__project_path__",
    "__is_development_mode__",
]
