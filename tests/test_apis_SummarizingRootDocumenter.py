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


def test_str_01(test_path):
    builder = uqbar.apis.APIBuilder(
        [test_path / "fake_package"],
        test_path / "docs",
        member_documenter_classes=[
            uqbar.apis.FunctionDocumenter,
            uqbar.apis.SummarizingClassDocumenter,
        ],
        module_documenter_class=uqbar.apis.SummarizingModuleDocumenter,
        root_documenter_class=uqbar.apis.SummarizingRootDocumenter,
    )
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
               :hidden:

               fake_package/index

            .. raw:: html

               <hr/>

            .. rubric:: :ref:`fake_package <fake-package>`
               :class: section-header

            .. raw:: html

               <hr/>

            .. rubric:: :ref:`fake_package.empty_module <fake-package--empty-module>`
               :class: section-header

            .. raw:: html

               <hr/>

            .. rubric:: :ref:`fake_package.empty_package <fake-package--empty-package>`
               :class: section-header

            .. raw:: html

               <hr/>

            .. rubric:: :ref:`fake_package.empty_package.empty <fake-package--empty-package--empty>`
               :class: section-header

            .. raw:: html

               <hr/>

            .. rubric:: :ref:`fake_package.enums <fake-package--enums>`
               :class: section-header

            .. raw:: html

               <hr/>

            .. rubric:: Enumerations
               :class: subsection-header

            .. autosummary::
               :nosignatures:

               ~fake_package.enums.FakeEnum

            .. raw:: html

               <hr/>

            .. rubric:: :ref:`fake_package.module <fake-package--module>`
               :class: section-header

            .. raw:: html

               <hr/>

            .. rubric:: Classes
               :class: subsection-header

            .. autosummary::
               :nosignatures:

               ~fake_package.module.ChildClass
               ~fake_package.module.PublicClass

            .. raw:: html

               <hr/>

            .. rubric:: Functions
               :class: subsection-header

            .. autosummary::
               :nosignatures:

               ~fake_package.module.public_function

            .. raw:: html

               <hr/>

            .. rubric:: :ref:`fake_package.multi <fake-package--multi>`
               :class: section-header

            .. raw:: html

               <hr/>

            .. rubric:: Classes
               :class: subsection-header

            .. autosummary::
               :nosignatures:

               ~fake_package.multi.PublicClass

            .. raw:: html

               <hr/>

            .. rubric:: Functions
               :class: subsection-header

            .. autosummary::
               :nosignatures:

               ~fake_package.multi.public_function

            .. raw:: html

               <hr/>

            .. rubric:: :ref:`fake_package.multi.one <fake-package--multi--one>`
               :class: section-header

            .. raw:: html

               <hr/>

            .. rubric:: Classes
               :class: subsection-header

            .. autosummary::
               :nosignatures:

               ~fake_package.multi.one.PublicClass

            .. raw:: html

               <hr/>

            .. rubric:: Functions
               :class: subsection-header

            .. autosummary::
               :nosignatures:

               ~fake_package.multi.one.public_function

            .. raw:: html

               <hr/>

            .. rubric:: :ref:`fake_package.multi.two <fake-package--multi--two>`
               :class: section-header

            .. raw:: html

               <hr/>

            .. rubric:: Classes
               :class: subsection-header

            .. autosummary::
               :nosignatures:

               ~fake_package.multi.two.PublicClass

            .. raw:: html

               <hr/>

            .. rubric:: Functions
               :class: subsection-header

            .. autosummary::
               :nosignatures:

               ~fake_package.multi.two.public_function
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

            .. container:: svg-container

               .. inheritance-diagram:: fake_package
                  :lineage: fake_package

            .. raw:: html

               <hr/>

            .. rubric:: Subpackages
               :class: section-header

            .. toctree::
               :hidden:

               empty_module
               empty_package/index
               enums
               module
               multi/index

            .. autosummary::
               :nosignatures:

               empty_module
               empty_package
               enums
               module
               multi
            """
        )
