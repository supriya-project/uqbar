import fake_package
import pathlib
import uqbar.apis

builder = uqbar.apis.APIBuilder(
    fake_package.__path__,
    pathlib.Path(__file__).parent / 'api',
    member_documenter_classes=[
        uqbar.apis.FunctionDocumenter,
        uqbar.apis.SummarizingClassDocumenter,
        ],
    module_documenter_class=uqbar.apis.SummarizingModuleDocumenter,
    root_documenter_class=uqbar.apis.SummarizingRootDocumenter,
    )
builder()

master_doc = 'index'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'uqbar.sphinx.inheritance',
    'uqbar.sphinx.style',
    ]

html_static_path = ['_static']
