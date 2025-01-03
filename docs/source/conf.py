# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'inkBoard'
copyright = '2024, Slalamander'
author = 'Slalamander'
release = '0.0.1'
html_theme = 'shibuya'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
            "sphinx.ext.autosectionlabel",
            "sphinx_copybutton",
            "sphinx_design",
            "sphinx_new_tab_link",
            "sphinx_carousel.carousel"
            ]

# templates_path = ['_templates']
html_static_path = ['_static']
html_css_files = [
    'custom.css',
]
exclude_patterns = []

html_title = "inkBoard"
html_logo = "_static/images/logo.svg"
html_favicon = "_static/images/favicon.ico"

highlight_language = "yaml"

# highlight_options = {
#     'default': {'stripall': True},
#     'php': {'startinline': True},
# }

navbar_links = [
        {
            "title": "Tutorial",
            "url": "tutorial/index",
            "children": [
                {
                    "title": "Cheatsheet",
                    "url": "tutorial/cheatsheet",
                    "summary": "A quick reference for core concepts"
                }
            ]
        },
        {
            "title": "Documentation",
            "url": "https://github.com/sponsors/lepture",
            "children": [
                {
                    "title": "Base Configuration",
                    "url": "config",
                    "summary": "Basic configuration components",
                }
            ]
        }
    ]

html_theme_options = {
    "accent_color": "blue",
    "github_url": "https://github.com/Slalamander/inkBoard",
    "nav_links": navbar_links
}

carousel_show_controls = True
carousel_show_indicators = True
carousel_show_buttons_on_top = False
carousel_show_captions_below = True

# intersphinx_mapping = {'pillow': ('https://pillow.readthedocs.io/en/stable', None)}