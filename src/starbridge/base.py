import importlib.metadata

__project_name__ = __name__.split(".")[0]
__version__ = importlib.metadata.version(__project_name__)

__all__ = ["__version__", "__project_name__"]
