import pathlib
import pytest
import shutil
import sys
import uqbar.apis
import uqbar.strings
from sphinx_testing import with_app


@pytest.fixture
def test_path():
    test_path = pathlib.Path(__file__).parent
    docs_path = test_path / 'docs'
    if str(test_path) not in sys.path:
        sys.path.insert(0, str(test_path))
    if docs_path.exists():
        shutil.rmtree(str(docs_path))
    builder = uqbar.apis.APIBuilder(
        [test_path / 'fake_package'],
        test_path / 'docs',
        member_documenter_classes=[
            uqbar.apis.FunctionDocumenter,
            uqbar.apis.SummarizingClassDocumenter,
            ],
        module_documenter_class=uqbar.apis.SummarizingModuleDocumenter,
        root_documenter_class=uqbar.apis.SummarizingRootDocumenter,
        )
    builder()
    with (docs_path / 'conf.py').open('w') as file_pointer:
        file_pointer.write(uqbar.strings.normalize('''
            # -*- coding: utf-8 -*-

            master_doc = 'index'

            extensions = [
                'sphinx.ext.autodoc',
                'sphinx.ext.autosummary',
                'uqbar.sphinx.style',
                ]

            html_static_path = ['_static']
            '''))
    (docs_path / '_static').mkdir(parents=True)
    yield test_path
    if docs_path.exists():
        shutil.rmtree(str(docs_path))


def test_foo(test_path):
    @with_app(
        buildername='html',
        srcdir=test_path / 'docs',
        copy_srcdir_to_tmpdir=False,
        )
    def execute(app, status, warning):
        app.build()
        results['app'] = app
        results['status'] = status.getvalue()
        results['warning'] = warning.getvalue()

    results = {}
    execute()
    assert 'build succeeded' in results['status']
    assert not results['warning'].strip()
