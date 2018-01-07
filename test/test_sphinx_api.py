import pathlib
import pytest
import shutil
import sys
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
    docs_path.mkdir()
    with (docs_path / 'conf.py').open('w') as file_pointer:
        file_pointer.write(uqbar.strings.normalize('''
            # -*- coding: utf-8 -*-

            master_doc = 'index'

            extensions = [
                'sphinx.ext.autodoc',
                'uqbar.sphinx.api',
                ]

            html_static_path = ['_static']

            uqbar_api_source_paths = ['fake_package']
            '''))
    with (docs_path / 'index.rst').open('w') as file_pointer:
        file_pointer.write(uqbar.strings.normalize('''
            Fake Docs
            =========

            .. toctree::

               api/index
            '''))
    (docs_path / '_static').mkdir(parents=True)
    yield test_path
    if docs_path.exists():
        shutil.rmtree(str(docs_path))


def test_foo(test_path):
    @with_app(
        buildername='text',
        srcdir=test_path / 'docs',
        copy_srcdir_to_tmpdir=False,
        )
    def execute(app, status, warning):
        app.build()
        results['app'] = app
        results['status'] = status.getvalue()
        results['warning'] = warning.getvalue()
        builddir = pathlib.Path(results['app'].builddir)
        text_path = builddir / 'text' / 'api' / 'index.txt'
        with text_path.open('r') as file_pointer:
            results['text'] = file_pointer.read()

    results = {}
    execute()
    assert 'build succeeded' in results['status']
    assert not results['warning'].strip()
    assert results['text'] == uqbar.strings.normalize('''
        ''')
