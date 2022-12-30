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
    documenter = uqbar.apis.SummarizingClassDocumenter(
        "fake_package.module.PublicClass"
    )
    assert normalize(str(documenter)) == normalize(
        """
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
        """
    )


def test_str_02(test_path):
    documenter = uqbar.apis.SummarizingClassDocumenter("fake_package.module.ChildClass")
    assert normalize(str(documenter)) == normalize(
        """
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
            """
    )


def test_str_03(test_path):
    documenter = uqbar.apis.SummarizingClassDocumenter(
        "fake_package.module._PrivateClass"
    )
    assert normalize(str(documenter)) == normalize(
        """
        .. autoclass:: _PrivateClass
        """
    )


def test_str_04(test_path):
    documenter = uqbar.apis.SummarizingClassDocumenter("fake_package.enums.FakeEnum")
    if sys.version_info.minor < 11:
        assert normalize(str(documenter)) == normalize(
            """
            .. autoclass:: FakeEnum
               :members:
               :undoc-members:
            """
        )
    else:
        assert normalize(str(documenter)) == normalize(
            """
            .. autoclass:: FakeEnum
               :members:
               :undoc-members:

               .. raw:: html

                  <hr/>

               .. rubric:: Special methods
                  :class: class-header

               .. container:: inherited

                  .. automethod:: FakeEnum.__abs__

               .. container:: inherited

                  .. automethod:: FakeEnum.__add__

               .. container:: inherited

                  .. automethod:: FakeEnum.__and__

               .. container:: inherited

                  .. automethod:: FakeEnum.__bool__

               .. container:: inherited

                  .. automethod:: FakeEnum.__ceil__

               .. container:: inherited

                  .. automethod:: FakeEnum.__contains__

               .. container:: inherited

                  .. automethod:: FakeEnum.__dir__

               .. container:: inherited

                  .. automethod:: FakeEnum.__divmod__

               .. container:: inherited

                  .. automethod:: FakeEnum.__eq__

               .. container:: inherited

                  .. automethod:: FakeEnum.__float__

               .. container:: inherited

                  .. automethod:: FakeEnum.__floor__

               .. container:: inherited

                  .. automethod:: FakeEnum.__floordiv__

               .. automethod:: FakeEnum.__format__

               .. container:: inherited

                  .. automethod:: FakeEnum.__ge__

               .. container:: inherited

                  .. automethod:: FakeEnum.__getitem__

               .. container:: inherited

                  .. automethod:: FakeEnum.__gt__

               .. container:: inherited

                  .. automethod:: FakeEnum.__hash__

               .. container:: inherited

                  .. automethod:: FakeEnum.__index__

               .. container:: inherited

               .. container:: inherited

                  .. automethod:: FakeEnum.__rrshift__

               .. container:: inherited

                  .. automethod:: FakeEnum.__rshift__

               .. container:: inherited

                  .. automethod:: FakeEnum.__rsub__

               .. container:: inherited

                  .. automethod:: FakeEnum.__rtruediv__

               .. container:: inherited

                  .. automethod:: FakeEnum.__rxor__

               .. container:: inherited

                  .. automethod:: FakeEnum.__str__

               .. container:: inherited

                  .. automethod:: FakeEnum.__sub__

               .. container:: inherited

                  .. automethod:: FakeEnum.__truediv__

               .. container:: inherited

                  .. automethod:: FakeEnum.__trunc__

               .. container:: inherited

                  .. automethod:: FakeEnum.__xor__

               .. raw:: html

                  <hr/>

               .. rubric:: Methods
                  :class: class-header

               .. container:: inherited

                  .. automethod:: FakeEnum.as_integer_ratio

               .. container:: inherited

                  .. automethod:: FakeEnum.bit_count

               .. container:: inherited

                  .. automethod:: FakeEnum.bit_length

               .. container:: inherited

                  .. automethod:: FakeEnum.conjugate

               .. container:: inherited

                  .. automethod:: FakeEnum.to_bytes

               .. raw:: html

                  <hr/>

               .. rubric:: Class & static methods
                  :class: class-header

               .. container:: inherited

                  .. automethod:: FakeEnum.from_bytes
            """
        )
