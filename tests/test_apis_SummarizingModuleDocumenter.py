import pathlib
import sys

import pytest

import uqbar.apis
from uqbar.strings import normalize


@pytest.fixture
def test_path():
    test_path = pathlib.Path(__file__).parent
    if str(test_path) not in sys.path:
        sys.path.insert(0, str(test_path))


def test_str_01(test_path):
    documenter = uqbar.apis.SummarizingModuleDocumenter("fake_package.module")
    assert normalize(str(documenter)) == normalize(
        """
        .. _fake-package--module:

        module
        ======

        .. automodule:: fake_package.module

        .. currentmodule:: fake_package.module

        .. container:: svg-container

           .. inheritance-diagram:: fake_package
              :lineage: fake_package.module

        .. raw:: html

           <hr/>

        .. rubric:: Classes
           :class: section-header

        .. autosummary::
           :nosignatures:

           ~ChildClass
           ~PublicClass

        .. autoclass:: ChildClass
           :members:
           :undoc-members:

        .. autoclass:: PublicClass
           :members:
           :undoc-members:

        .. raw:: html

           <hr/>

        .. rubric:: Functions
           :class: section-header

        .. autosummary::
           :nosignatures:

           ~public_function

        .. autofunction:: public_function
        """
    )


def test_str_02(test_path):
    documenter = uqbar.apis.SummarizingModuleDocumenter(
        "fake_package.module", document_private_members=True
    )
    assert normalize(str(documenter)) == normalize(
        """
        .. _fake-package--module:

        module
        ======

        .. automodule:: fake_package.module

        .. currentmodule:: fake_package.module

        .. container:: svg-container

           .. inheritance-diagram:: fake_package
              :lineage: fake_package.module

        .. raw:: html

           <hr/>

        .. rubric:: Classes
           :class: section-header

        .. autosummary::
           :nosignatures:

           ~ChildClass
           ~PublicClass
           ~_PrivateClass

        .. autoclass:: ChildClass
           :members:
           :undoc-members:

        .. autoclass:: PublicClass
           :members:
           :undoc-members:

        .. autoclass:: _PrivateClass
           :members:
           :undoc-members:

        .. raw:: html

           <hr/>

        .. rubric:: Functions
           :class: section-header

        .. autosummary::
           :nosignatures:

           ~_private_function
           ~public_function

        .. autofunction:: _private_function

        .. autofunction:: public_function
        """
    )


def test_str_03(test_path):
    documenter = uqbar.apis.SummarizingModuleDocumenter(
        "fake_package.module",
        member_documenter_classes=[
            uqbar.apis.FunctionDocumenter,
            uqbar.apis.SummarizingClassDocumenter,
        ],
    )
    assert normalize(str(documenter)) == normalize(
        """
        .. _fake-package--module:

        module
        ======

        .. automodule:: fake_package.module

        .. currentmodule:: fake_package.module

        .. container:: svg-container

           .. inheritance-diagram:: fake_package
              :lineage: fake_package.module

        .. raw:: html

           <hr/>

        .. rubric:: Classes
           :class: section-header

        .. autosummary::
           :nosignatures:

           ~ChildClass
           ~PublicClass

        .. autoclass:: ChildClass

           .. raw:: html

              <hr/>

           .. rubric:: Attributes Summary
              :class: class-header

           .. autosummary::
              :nosignatures:

              inheritable_method
              new_method

           .. raw:: html

              <hr/>

           .. rubric:: Special methods
              :class: class-header

           .. container:: inherited

              .. automethod:: ChildClass.__str__

           .. raw:: html

              <hr/>

           .. rubric:: Methods
              :class: class-header

           .. automethod:: ChildClass.inheritable_method

           .. container:: inherited

              .. automethod:: ChildClass.method

           .. automethod:: ChildClass.new_method

           .. container:: inherited

              .. automethod:: ChildClass.other_method

           .. raw:: html

              <hr/>

           .. rubric:: Class & static methods
              :class: class-header

           .. container:: inherited

              .. automethod:: ChildClass.class_method

           .. container:: inherited

              .. automethod:: ChildClass.static_method

           .. raw:: html

              <hr/>

           .. rubric:: Read/write properties
              :class: class-header

           .. container:: inherited

              .. autoattribute:: ChildClass.read_write_property

           .. raw:: html

              <hr/>

           .. rubric:: Read-only properties
              :class: class-header

           .. container:: inherited

              .. autoattribute:: ChildClass.read_only_property

        .. autoclass:: PublicClass

           .. raw:: html

              <hr/>

           .. rubric:: Attributes Summary
              :class: class-header

           .. autosummary::
              :nosignatures:

              __str__
              class_method
              inheritable_method
              method
              other_method
              read_only_property
              read_write_property
              static_method

           .. raw:: html

              <hr/>

           .. rubric:: Special methods
              :class: class-header

           .. automethod:: PublicClass.__str__

           .. raw:: html

              <hr/>

           .. rubric:: Methods
              :class: class-header

           .. automethod:: PublicClass.inheritable_method

           .. automethod:: PublicClass.method

           .. automethod:: PublicClass.other_method

           .. raw:: html

              <hr/>

           .. rubric:: Class & static methods
              :class: class-header

           .. automethod:: PublicClass.class_method

           .. automethod:: PublicClass.static_method

           .. raw:: html

              <hr/>

           .. rubric:: Read/write properties
              :class: class-header

           .. autoattribute:: PublicClass.read_write_property

           .. raw:: html

              <hr/>

           .. rubric:: Read-only properties
              :class: class-header

           .. autoattribute:: PublicClass.read_only_property

        .. raw:: html

           <hr/>

        .. rubric:: Functions
           :class: section-header

        .. autosummary::
           :nosignatures:

           ~public_function

        .. autofunction:: public_function
        """
    )
