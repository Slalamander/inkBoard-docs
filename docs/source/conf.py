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
            "sphinx_carousel.carousel",
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

carousel_show_controls = True
carousel_show_indicators = True
carousel_show_buttons_on_top = False
carousel_show_captions_below = True

# exclude_patterns = ["documentation/*.rst"]

# intersphinx_mapping = {'pillow': ('https://pillow.readthedocs.io/en/stable', None)}

##This is from a monkey path fix, found here: https://github.com/sphinx-doc/sphinx/issues/6676#issuecomment-531891618
def convert_docutils_node(list_item):
    if not list_item.children:
        return None
    reference = list_item.children[0]
    title = reference.children[0].astext()
    url = reference.attributes['refuri']
    active = 'current' in list_item.attributes['classes']

    nav = {}
    nav['title'] = title
    nav['url'] = url
    nav['children'] = []
    nav['active'] = active

    if len(list_item.children) > 1:
        for child_item in list_item.children[1].children:
            child_nav = convert_docutils_node(child_item)
            if child_nav is not None:
                nav['children'].append(child_nav)

    return nav


def update_page_context(self, pagename, templatename, ctx, event_arg):
    print("UPDATING PAGE CONTEXT THINGY")
    from sphinx.environment.adapters.toctree import TocTree

    def get_nav_object(**kwds):
        toctree = TocTree(self.env).get_toctree_for(
            pagename, self, collapse=True, **kwds)

        nav = []
        for child in toctree.children[0].children:
            child_nav = convert_docutils_node(child)
            nav.append(child_nav)

        return nav

    def get_page_toc_object():
        self_toc = TocTree(self.env).get_toc_for(pagename, self)
        toc = self.render_partial(self_toc)['fragment']

        try:
            nav = convert_docutils_node(self_toc.children[0])
            return nav
        except:
            return {}

    ctx['get_nav_object'] = get_nav_object
    ctx['get_page_toc_object'] = get_page_toc_object
    return None


import sphinx.builders.html
sphinx.builders.html.StandaloneHTMLBuilder.update_page_context = update_page_context