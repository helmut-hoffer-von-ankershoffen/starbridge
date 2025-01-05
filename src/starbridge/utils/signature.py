"""Original source: https://github.com/pydantic/pydantic-ai/blob/main/pydantic_ai_slim/pydantic_ai/_griffe.py."""

from __future__ import annotations as _annotations

import re
from inspect import Parameter, signature
from typing import TYPE_CHECKING, Any, Literal, cast

from griffe import Docstring, DocstringSectionKind
from griffe import Object as GriffeObject

if TYPE_CHECKING:
    from collections.abc import Callable

DocstringStyle = Literal["google", "numpy", "sphinx"]


def description_and_params(  # noqa: C901
    func: Callable[..., Any],
    excluded_params: tuple[str, ...] = ("self", "context"),
) -> tuple[str, list, dict[str, dict]]:
    """
    Extract the function description and parameter descriptions from a function's docstring.

    Args:
        func: The function to extract descriptions from.
        excluded_params: A tuple of parameter names to exclude from the result.

    Returns:
        A tuple of (main function description, parameter properties dict).

    """
    doc = func.__doc__
    if doc is None:
        return func.__name__, [], {}

    sig = signature(func)

    # see https://github.com/mkdocstrings/griffe/issues/293
    parent = cast("GriffeObject", sig)

    docstring = Docstring(
        doc,
        lineno=1,
        parser=_infer_docstring_style(doc),
        parent=parent,
    )
    sections = docstring.parse()

    # Get parameter descriptions from docstring
    param_desc = {}
    if parameters := next(
        (p for p in sections if p.kind == DocstringSectionKind.parameters),
        None,
    ):
        param_desc = {p.name: p.description for p in parameters.value}

    # Build parameter properties including type info
    params = {}
    required = []
    for param in sig.parameters.values():
        if param.name in excluded_params:
            continue

        param_type = "string"  # default type
        if param.annotation != Parameter.empty:
            if param.annotation is str:
                param_type = "string"
            elif param.annotation is int:
                param_type = "number"
            elif param.annotation is bool:
                param_type = "boolean"

        if param.default == Parameter.empty:
            required.append(param.name)

        params[param.name] = {
            "type": param_type,
            "description": param_desc.get(param.name, f"Parameter {param.name}"),
        }

    main_desc = ""
    if main := next((p for p in sections if p.kind == DocstringSectionKind.text), None):
        main_desc = main.value

    return main_desc, required, params


def _infer_docstring_style(doc: str) -> DocstringStyle:
    """
    Simplistic docstring style inference.

    Args:
        doc: The docstring to analyze

    Returns:
        DocstringStyle: The inferred docstring style ('google', 'numpy', or 'sphinx')

    """
    for pattern, replacements, style in _docstring_style_patterns:
        matches = (
            re.search(pattern.format(replacement), doc, re.IGNORECASE | re.MULTILINE) for replacement in replacements
        )
        if any(matches):
            return style
    # fallback to google style
    return "google"


# See https://github.com/mkdocstrings/griffe/issues/329#issuecomment-2425017804
_docstring_style_patterns: list[tuple[str, list[str], DocstringStyle]] = [
    (
        r"\n[ \t]*:{0}([ \t]+\w+)*:([ \t]+.+)?\n",
        [
            "param",
            "parameter",
            "arg",
            "argument",
            "key",
            "keyword",
            "type",
            "var",
            "ivar",
            "cvar",
            "vartype",
            "returns",
            "return",
            "rtype",
            "raises",
            "raise",
            "except",
            "exception",
        ],
        "sphinx",
    ),
    (
        r"\n[ \t]*{0}:([ \t]+.+)?\n[ \t]+.+",
        [
            "args",
            "arguments",
            "params",
            "parameters",
            "keyword args",
            "keyword arguments",
            "other args",
            "other arguments",
            "other params",
            "other parameters",
            "raises",
            "exceptions",
            "returns",
            "yields",
            "receives",
            "examples",
            "attributes",
            "functions",
            "methods",
            "classes",
            "modules",
            "warns",
            "warnings",
        ],
        "google",
    ),
    (
        r"\n[ \t]*{0}\n[ \t]*---+\n",
        [
            "deprecated",
            "parameters",
            "other parameters",
            "returns",
            "yields",
            "receives",
            "raises",
            "warns",
            "attributes",
            "functions",
            "methods",
            "classes",
            "modules",
        ],
        "numpy",
    ),
]
