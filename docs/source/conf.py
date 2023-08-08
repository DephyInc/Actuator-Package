# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


# For configuration of the pydata theme, see this example:
# https://github.com/martinfleis/momepy/tree/main/docs

import flexsea

project = "flexsea"
copyright = "2023, Dephy, Inc."  # pylint: disable=W0622
author = "Dephy, Inc."
release = flexsea.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "boto3": ("https://boto3.amazonaws.com/v1/documentation/api/latest/", None),
}

templates_path = ["_templates"]
exclude_patterns = []
add_function_parentheses = False
today_fmt = "%B %d, %Y"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_logo = "_static/logo-dephy.png"
html_theme_options = {
    "github_url": "https://github.com/DephyInc/Actuator-Package",
    "collapse_navigation": True,
    "pygment_light_style": "lovelace",
    "pygment_dark_style": "nord",
    "header_links_before_dropdown": 6,
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    "logo": {
        "image_light": "logo-dephy.png",
        "image_dark": "logo-dephy.png",
    },
}
html_static_path = ["_static"]
html_favicon = "_static/favicon-16x16.png"


def setup(app):
    app.add_css_file("custom.css")
