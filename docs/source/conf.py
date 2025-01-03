# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "starbridge"
copyright = "2025, Helmut Hoffer von Ankershoffen"
author = "Helmut Hoffer von Ankershoffen"
release = "0.0.67"
github_username = "helmut-hoffer-von-ankershoffen"
github_repository = "starbridge"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx_autodoc_typehints",
    "sphinx-pydantic",
    "sphinxcontrib.autodoc_pydantic",
    "enum_tools.autoenum",
    "sphinx_copybutton",
    "sphinx.ext.coverage",
    "sphinx_mdinclude",
    "sphinxext.opengraph",
    "sphinx_inline_tabs",
    "sphinx_toolbox",
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
html_logo = "../../starbridge.png"
html_theme_options = {
    "announcement": (
        '<a target="_blank" href="https://github.com/helmut-hoffer-von-ankershoffen/starbridge">GitHub</a> - '
        '<a target="_blank" href="https://pypi.org/project/starbridge/">PyPI</a> - '
        '<a target="_blank" href="https://hub.docker.com/r/helmuthva/starbridge/tags">Docker</a> - '
        '<a target="_blank" href="https://sonarcloud.io/summary/new_code?id=helmut-hoffer-von-ankershoffen_starbridge">SonarQube</a> - '
        '<a target="_blank" href="https://app.codecov.io/gh/helmut-hoffer-von-ankershoffen/starbridge">Codecov</a>'
    )
}
