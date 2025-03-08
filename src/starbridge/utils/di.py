"""Module for dynamic import and discovery of implementations and subclasses."""

import importlib
import pkgutil
from inspect import isclass
from typing import Any

from starbridge import __project_name__

_implementation_cache = {}
_subclass_cache = {}


def locate_implementations(_class: type[Any]) -> list[Any]:
    """
    Dynamically discover all Service classes in starbridge packages.

    Args:
        _class (type[Any]): Class to search for.

    Returns:
        list[Any]: List of discovered implementations of the given class.

    """
    if _class in _implementation_cache:
        return _implementation_cache[_class]

    implementations = []
    package = importlib.import_module(__project_name__)

    for _, name, _ in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f"{__project_name__}.{name}")
        # Check all members of the module
        for member_name in dir(module):
            member = getattr(module, member_name)
            if isinstance(member, _class):
                implementations.append(member)

    _implementation_cache[_class] = implementations
    return implementations


def locate_subclasses(_class: type[Any]) -> list[type[Any]]:
    """
    Dynamically discover all Service classes in starbridge packages.

    Args:
        _class (type[Any]): Parent class of subclasses to search for.

    Returns:
        list[type[Any]]: List of discovered subclasses of the given class.

    """
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
