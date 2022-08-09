import datetime

import uqbar

### SPHINX ###

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.graphviz",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    # "sphinx.ext.viewcode",
    "uqbar.sphinx.api",
    "uqbar.sphinx.book",
    "uqbar.sphinx.inheritance",
    "sphinx_immaterial"
]

add_module_names = False
author = "Josiah Wolf Oberholtzer"
copyright = f"2017-{datetime.date.today().year}, Josiah Wolf Oberholtzer"
exclude_patterns = []
htmlhelp_basename = "uqbardoc"
language = "en"
master_doc = "index"
project = "Uqbar"
pygments_style = "sphinx"
source_suffix = ".rst"
templates_path = ["_templates"]
version = release = uqbar.__version__

### GRAPHVIZ ###

graphviz_output_format = "svg"

### INTERSPHINX ###

intersphinx_mapping = {
    "https://docs.python.org/3.6/": None,
    "http://www.sphinx-doc.org/en/stable/": None,
}

### THEME ###

html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css",
]
html_domain_indices = True
html_favicon = "favicon.ico"
html_js_files = []
html_logo = "icon.svg"
html_static_path = ["_static"]
html_theme = "sphinx_immaterial"
html_theme_options = {
    "icon": {
        "repo": "fontawesome/brands/github",
    },
    "site_url": "https://josiahwolfoberholtzer.com/uqbar/",
    "repo_url": "https://github.com/josiah-wolf-oberholtzer/uqbar/",
    "repo_name": "uqbar",
    "repo_type": "github",
    "edit_uri": "blob/main/docs",
    "globaltoc_collapse": True,
    "features": [
        # "header.autohide",
        "navigation.expand",
        # "navigation.instant",
        # "navigation.sections",
        "navigation.tabs",
        "navigation.top",
        # "search.highlight",
        # "search.share",
        # "toc.integrate",
    ],
    "palette": [
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "blue-grey",
            "accent": "lime",
            "toggle": {
                "icon": "material/toggle-switch",
                "name": "Switch to light mode",
            },
        },
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "indigo",
            "accent": "teal",
            "toggle": {
                "icon": "material/toggle-switch-off-outline",
                "name": "Switch to dark mode",
            },
        },
    ],
    "version_dropdown": False,
}
html_title = "Uqbar"
html_use_index = True

### UQBAR API ###

uqbar_api_member_documenter_classes = [
    "uqbar.apis.FunctionDocumenter",
    "uqbar.apis.ImmaterialClassDocumenter",
]
uqbar_api_module_documenter_class = "uqbar.apis.ImmaterialModuleDocumenter"
uqbar_api_root_documenter_class = "uqbar.apis.SummarizingRootDocumenter"
uqbar_api_source_paths = uqbar.__path__
uqbar_api_title = "Uqbar API"

### UQBAR BOOK ###

uqbar_book_strict = True
uqbar_book_use_black = True
