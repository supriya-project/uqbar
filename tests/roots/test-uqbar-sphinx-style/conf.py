master_doc = "index"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "uqbar.sphinx.api",
    "uqbar.sphinx.inheritance",
    "uqbar.sphinx.style",
]

html_static_path = ["_static"]

uqbar_api_source_paths = ["fake_package"]
uqbar_api_module_documenter_class = "uqbar.apis.SummarizingModuleDocumenter"
uqbar_api_member_documenter_classes = [
    "uqbar.apis.FunctionDocumenter",
    "uqbar.apis.SummarizingClassDocumenter",
]
