import pathlib
import pytest
import sys
import uqbar.apis
from uqbar.strings import normalize


@pytest.fixture
def test_path():
    test_path = pathlib.Path(__file__).parent
    if str(test_path) not in sys.path:
        sys.path.insert(0, str(test_path))


def test_str_01(test_path):
    documenter = uqbar.apis.SummarizingClassDocumenter(
        'fake_package.module.PublicClass')
    assert normalize(str(documenter)) == normalize('''
        .. autoclass:: PublicClass

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

           .. automethod:: PublicClass.inheritable_class_method

           .. automethod:: PublicClass.inheritable_static_method

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
        ''')


def test_str_02(test_path):
    documenter = uqbar.apis.SummarizingClassDocumenter(
        'fake_package.module.ChildClass')
    assert normalize(str(documenter)) == normalize('''
        .. autoclass:: ChildClass

           .. raw:: html

              <hr/>

           .. rubric:: Special methods
              :class: class-header

           .. automethod:: ChildClass.__str__

           .. raw:: html

              <hr/>

           .. rubric:: Methods
              :class: class-header

           .. automethod:: ChildClass.inheritable_method

           .. automethod:: ChildClass.method

           .. automethod:: ChildClass.new_method

           .. automethod:: ChildClass.other_method

           .. raw:: html

              <hr/>

           .. rubric:: Class & static methods
              :class: class-header

           .. automethod:: ChildClass.class_method

           .. automethod:: ChildClass.inheritable_class_method

           .. automethod:: ChildClass.inheritable_static_method

           .. automethod:: ChildClass.static_method

           .. raw:: html

              <hr/>

           .. rubric:: Read/write properties
              :class: class-header

           .. autoattribute:: ChildClass.read_write_property

           .. raw:: html

              <hr/>

           .. rubric:: Read-only properties
              :class: class-header

           .. autoattribute:: ChildClass.read_only_property
            ''')


def test_str_03(test_path):
    documenter = uqbar.apis.SummarizingClassDocumenter(
        'fake_package.module._PrivateClass')
    assert normalize(str(documenter)) == normalize('''
        .. autoclass:: _PrivateClass
        ''')
