import os
import pathlib
import shutil
import sys

import pytest

import uqbar.apis
from uqbar.strings import normalize


@pytest.fixture
def test_path():
    test_path = pathlib.Path(__file__).parent
    docs_path = test_path / "docs"
    if str(test_path) not in sys.path:
        sys.path.insert(0, str(test_path))
    if docs_path.exists():
        shutil.rmtree(str(docs_path))
    yield test_path
    if docs_path.exists():
        shutil.rmtree(str(docs_path))


def test_collection_01(test_path):
    builder = uqbar.apis.APIBuilder([test_path / "fake_package"], test_path / "docs")
    source_paths = uqbar.apis.collect_source_paths(builder._initial_source_paths)
    node_tree = builder.build_node_tree(source_paths)
    assert normalize(str(node_tree)) == normalize(
        """
        None/
            fake_package/
                fake_package.empty_module
                fake_package.empty_package/
                    fake_package.empty_package.empty
                fake_package.enums
                fake_package.module
                fake_package.multi/
                    fake_package.multi.one
                    fake_package.multi.two
        """
    )
    documenters = list(builder.collect_module_documenters(node_tree))
    assert isinstance(documenters[0], uqbar.apis.RootDocumenter)
    assert [documenter.package_path for documenter in documenters[1:]] == [
        "fake_package",
        "fake_package.empty_module",
        "fake_package.empty_package",
        "fake_package.empty_package.empty",
        "fake_package.enums",
        "fake_package.module",
        "fake_package.multi",
        "fake_package.multi.one",
        "fake_package.multi.two",
    ]


def test_collection_02(test_path):
    builder = uqbar.apis.APIBuilder(
        [test_path / "fake_package"], test_path / "docs", document_private_modules=True
    )
    source_paths = uqbar.apis.collect_source_paths(builder._initial_source_paths)
    node_tree = builder.build_node_tree(source_paths)
    assert normalize(str(node_tree)) == normalize(
        """
        None/
            fake_package/
                fake_package._private/
                    fake_package._private.nested
                fake_package.empty_module
                fake_package.empty_package/
                    fake_package.empty_package.empty
                fake_package.enums
                fake_package.module
                fake_package.multi/
                    fake_package.multi.one
                    fake_package.multi.two
        """
    )
    documenters = list(builder.collect_module_documenters(node_tree))
    assert isinstance(documenters[0], uqbar.apis.RootDocumenter)
    assert [documenter.package_path for documenter in documenters[1:]] == [
        "fake_package",
        "fake_package._private",
        "fake_package._private.nested",
        "fake_package.empty_module",
        "fake_package.empty_package",
        "fake_package.empty_package.empty",
        "fake_package.enums",
        "fake_package.module",
        "fake_package.multi",
        "fake_package.multi.one",
        "fake_package.multi.two",
    ]


def test_collection_03(test_path):
    builder = uqbar.apis.APIBuilder(
        [test_path / "fake_package" / "multi"], test_path / "docs"
    )
    source_paths = uqbar.apis.collect_source_paths(builder._initial_source_paths)
    node_tree = builder.build_node_tree(source_paths)
    documenters = list(builder.collect_module_documenters(node_tree))
    assert isinstance(documenters[0], uqbar.apis.RootDocumenter)
    assert [documenter.package_path for documenter in documenters[1:]] == [
        "fake_package",
        "fake_package.multi",
        "fake_package.multi.one",
        "fake_package.multi.two",
    ]


def test_collection_04(test_path):
    builder = uqbar.apis.APIBuilder(
        [test_path / "fake_package"], test_path / "docs", document_empty_modules=False
    )
    source_paths = uqbar.apis.collect_source_paths(builder._initial_source_paths)
    node_tree = builder.build_node_tree(source_paths)
    assert normalize(str(node_tree)) == normalize(
        """
        None/
            fake_package/
                fake_package.enums
                fake_package.module
                fake_package.multi/
                    fake_package.multi.one
                    fake_package.multi.two
        """
    )
    documenters = list(builder.collect_module_documenters(node_tree))
    assert isinstance(documenters[0], uqbar.apis.RootDocumenter)
    assert [documenter.package_path for documenter in documenters[1:]] == [
        "fake_package",
        "fake_package.enums",
        "fake_package.module",
        "fake_package.multi",
        "fake_package.multi.one",
        "fake_package.multi.two",
    ]


def test_output_01(test_path):
    builder = uqbar.apis.APIBuilder([test_path / "fake_package"], test_path / "docs")
    builder()
    paths = sorted((test_path / "docs").rglob("*"))
    paths = [
        str(path.relative_to(test_path)).replace(os.path.sep, "/") for path in paths
    ]
    assert paths == [
        "docs/fake_package",
        "docs/fake_package/empty_module.rst",
        "docs/fake_package/empty_package",
        "docs/fake_package/empty_package/empty.rst",
        "docs/fake_package/empty_package/index.rst",
        "docs/fake_package/enums.rst",
        "docs/fake_package/index.rst",
        "docs/fake_package/module.rst",
        "docs/fake_package/multi",
        "docs/fake_package/multi/index.rst",
        "docs/fake_package/multi/one.rst",
        "docs/fake_package/multi/two.rst",
        "docs/index.rst",
    ]
    base_path = test_path / "docs" / "fake_package"
    with (base_path / ".." / "index.rst").open() as file_pointer:
        assert normalize(file_pointer.read()) == normalize(
            """
            API
            ===

            .. toctree::

               fake_package/index
            """
        )
    with (base_path / "index.rst").open() as file_pointer:
        assert normalize(file_pointer.read()) == normalize(
            """
            .. _fake-package:

            fake_package
            ============

            .. automodule:: fake_package

            .. currentmodule:: fake_package

            .. toctree::

               empty_module
               empty_package/index
               enums
               module
               multi/index
            """
        )
    with (base_path / "module.rst").open() as file_pointer:
        assert normalize(file_pointer.read()) == normalize(
            """
            .. _fake-package--module:

            module
            ======

            .. automodule:: fake_package.module

            .. currentmodule:: fake_package.module

            .. autoclass:: ChildClass
               :members:
               :undoc-members:

            .. autoclass:: PublicClass
               :members:
               :undoc-members:

            .. autofunction:: public_function
            """
        )


def test_output_02(test_path):
    builder = uqbar.apis.APIBuilder(
        [test_path / "fake_package"], test_path / "docs", document_private_modules=True
    )
    builder()
    paths = sorted((test_path / "docs").rglob("*"))
    paths = [
        str(path.relative_to(test_path)).replace(os.path.sep, "/") for path in paths
    ]
    assert paths == [
        "docs/fake_package",
        "docs/fake_package/_private",
        "docs/fake_package/_private/index.rst",
        "docs/fake_package/_private/nested.rst",
        "docs/fake_package/empty_module.rst",
        "docs/fake_package/empty_package",
        "docs/fake_package/empty_package/empty.rst",
        "docs/fake_package/empty_package/index.rst",
        "docs/fake_package/enums.rst",
        "docs/fake_package/index.rst",
        "docs/fake_package/module.rst",
        "docs/fake_package/multi",
        "docs/fake_package/multi/index.rst",
        "docs/fake_package/multi/one.rst",
        "docs/fake_package/multi/two.rst",
        "docs/index.rst",
    ]
    base_path = test_path / "docs" / "fake_package"
    with (base_path / ".." / "index.rst").open() as file_pointer:
        assert normalize(file_pointer.read()) == normalize(
            """
            API
            ===

            .. toctree::

               fake_package/index
            """
        )
    with (base_path / "index.rst").open() as file_pointer:
        assert normalize(file_pointer.read()) == normalize(
            """
            .. _fake-package:

            fake_package
            ============

            .. automodule:: fake_package

            .. currentmodule:: fake_package

            .. toctree::

               _private/index
               empty_module
               empty_package/index
               enums
               module
               multi/index
            """
        )
    with (base_path / "module.rst").open() as file_pointer:
        assert normalize(file_pointer.read()) == normalize(
            """
            .. _fake-package--module:

            module
            ======

            .. automodule:: fake_package.module

            .. currentmodule:: fake_package.module

            .. autoclass:: ChildClass
               :members:
               :undoc-members:

            .. autoclass:: PublicClass
               :members:
               :undoc-members:

            .. autofunction:: public_function
            """
        )


def test_output_03(test_path):
    builder = uqbar.apis.APIBuilder(
        [test_path / "fake_package"],
        test_path / "docs",
        document_private_members=True,
        document_private_modules=True,
    )
    builder()
    paths = sorted((test_path / "docs").rglob("*"))
    paths = [
        str(path.relative_to(test_path)).replace(os.path.sep, "/") for path in paths
    ]
    assert paths == [
        "docs/fake_package",
        "docs/fake_package/_private",
        "docs/fake_package/_private/index.rst",
        "docs/fake_package/_private/nested.rst",
        "docs/fake_package/empty_module.rst",
        "docs/fake_package/empty_package",
        "docs/fake_package/empty_package/empty.rst",
        "docs/fake_package/empty_package/index.rst",
        "docs/fake_package/enums.rst",
        "docs/fake_package/index.rst",
        "docs/fake_package/module.rst",
        "docs/fake_package/multi",
        "docs/fake_package/multi/index.rst",
        "docs/fake_package/multi/one.rst",
        "docs/fake_package/multi/two.rst",
        "docs/index.rst",
    ]
    base_path = test_path / "docs" / "fake_package"
    with (base_path / ".." / "index.rst").open() as file_pointer:
        assert normalize(file_pointer.read()) == normalize(
            """
            API
            ===

            .. toctree::

               fake_package/index
            """
        )
    with (base_path / "index.rst").open() as file_pointer:
        assert normalize(file_pointer.read()) == normalize(
            """
            .. _fake-package:

            fake_package
            ============

            .. automodule:: fake_package

            .. currentmodule:: fake_package

            .. toctree::

               _private/index
               empty_module
               empty_package/index
               enums
               module
               multi/index
            """
        )
    with (base_path / "module.rst").open() as file_pointer:
        assert normalize(file_pointer.read()) == normalize(
            """
            .. _fake-package--module:

            module
            ======

            .. automodule:: fake_package.module

            .. currentmodule:: fake_package.module

            .. autoclass:: ChildClass
               :members:
               :undoc-members:

            .. autoclass:: PublicClass
               :members:
               :undoc-members:

            .. autoclass:: _PrivateClass
               :members:
               :undoc-members:

            .. autofunction:: _private_function

            .. autofunction:: public_function
            """
        )
