import importlib
import pkgutil
from inspect import isclass
from typing import Any

from starbridge import __project_name__

_implementation_cache = {}
_subclass_cache = {}


def locate_implementations(_class: Any) -> list[Any]:
    """Dynamically discover all Service classes in starbridge packages."""
    if _class in _implementation_cache:
        return _implementation_cache[_class]

    implementations = []
    package = importlib.import_module(__project_name__)

    for _, name, _ in pkgutil.iter_modules(package.__path__):
        try:
            module = importlib.import_module(f"{__project_name__}.{name}")
            # Check all members of the module
            for member_name in dir(module):
                member = getattr(module, member_name)
                if isinstance(member, _class):
                    implementations.append(member)
        except ImportError:
            continue

    _implementation_cache[_class] = implementations
    return implementations


def locate_subclasses(_class: Any) -> list[Any]:
    """Dynamically discover all Service classes in starbridge packages."""
    if _class in _subclass_cache:
        return _subclass_cache[_class]

    subclasses = []
    package = importlib.import_module(__project_name__)

    for _, name, _ in pkgutil.iter_modules(package.__path__):
        try:
            module = importlib.import_module(f"{__project_name__}.{name}")
            # Check all members of the module
            for member_name in dir(module):
                member = getattr(module, member_name)
                if isclass(member) and issubclass(member, _class) and member != _class:
                    subclasses.append(member)
        except ImportError:
            continue

    _subclass_cache[_class] = subclasses
    return subclasses
