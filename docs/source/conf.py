# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os
from pathlib import Path
from typing import TYPE_CHECKING
from sphinx.environment.adapters.toctree import _resolve_toctree, addnodes
from sphinx.builders.html import global_toctree_for_doc as sphinx_global_toctree_for_doc
from sphinx.builders import html

if TYPE_CHECKING:
    from sphinx.environment.adapters.toctree import BuildEnvironment, Builder, Element, _resolve_toctree, addnodes

# p = Path("./_extensions")
# a = p.absolute()
sys.path.append(os.path.abspath("./_extensions"))

project = 'inkBoard'
copyright = '2024, Slalamander'
author = 'Slalamander'
release = '0.0.1'
html_theme = 'shibuya'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
            "sphinx.ext.autosectionlabel",
            "sphinx.ext.napoleon",
            "sphinx.ext.autodoc",
            "sphinx_copybutton",
            "sphinx_design",
            "sphinx_new_tab_link",
            "sphinx_carousel.carousel",
            "myst_parser",

            "sphinx_replace_htmlpage_toctree",
            "ib_element_directive"
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
            "url": "/tutorial/index",
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
            "url": "documentation/index",
            "children": [
                {
                    "title": "Configuration",
                    "url": "documentation/configuration",
                },
                {
                    "title": "Elements",
                    "url": "elements/index",
                },
                {
                    "title": "Platforms",
                    "url": "platforms/index",
                },
                {
                    "title": "Integrations",
                    "url": "integrations/index",
                }
            ]
        }
    ]

html_theme_options = {
    "accent_color": "blue",
    "github_url": "https://github.com/Slalamander/inkBoard",
    "nav_links": navbar_links,
    "toctree_includehidden": False
}

html_sidebars = {
    "**": [
        "sidebars/localtoc.html",
        "sidebars/repo-stats.html"
    ]
    # "/tutorial/index": ["/_static/tutorialtoc.html"]
}

html_context = {
    "source_type": "github",
    "source_user": "Slalamander",
    "source_repo": "inkBoard",
}

autosectionlabel_prefix_document = True

python_display_short_literal_types = True
add_module_names = False

napoleon_include_special_with_doc = False

autodoc_class_signature = "separated"
# autodoc_typehints = "description"

carousel_show_controls = True
carousel_show_indicators = True
carousel_show_buttons_on_top = False
carousel_show_captions_below = True

# exclude_patterns = ["documentation/*.rst"]

# intersphinx_mapping = {'pillow': ('https://pillow.readthedocs.io/en/stable', None)}

replace_global_tocs = {
    "tutorial/*": "tutorialtree",
    "documentation/*": "docstree",
    "elements/*": "docstree",
    "platforms/*": "docstree",
    "integrations/*": "docstree",
}

def global_toctree_for_doc(
    env: "BuildEnvironment",
    docname: "str",
    builder: Builder,
    collapse: bool = False,
    includehidden: bool = True,
    maxdepth: int = 0,
    titles_only: bool = False,
) -> "Element" | None:
    """Get the global ToC tree at a given document.

    This gives the global ToC, with all ancestors and their siblings.
    """
    ##Some refs regarding fixing to ToC:
    ##A monkey path fix that put me on the right path: https://github.com/sphinx-doc/sphinx/issues/6676#issuecomment-531891618
    ##Maybe see if it can be removed via the toc builder by dealing with overwriting that
    ##Another comment by someone: https://github.com/pradyunsg/sphinx-basic-ng/issues/16#issuecomment-836587466
    
    resolved = (
        _resolve_toctree(
            env,
            docname,
            builder,
            toctree_node,
            prune=True,
            maxdepth=int(maxdepth),
            titles_only=titles_only,
            collapse=collapse,
            includehidden=includehidden,
        )
        for toctree_node in env.master_doctree.findall(addnodes.toctree)
    )
    toctrees = [toctree for toctree in resolved if toctree is not None]

    if not toctrees:
        return None

    ##Like this the toc should work as I want it to.
    ##But it is hardcoded in terms of the order they appear in.
    if "tutorial/" in docname:
        result = toctrees[0]
    else:
        result = toctrees[1]
        toctrees = toctrees[2:]
        for toctree in toctrees[2:]:
            result.extend(toctree.children)
    return result

# html.global_toctree_for_doc = global_toctree_for_doc

