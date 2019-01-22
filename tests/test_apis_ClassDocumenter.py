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
    documenter = uqbar.apis.ClassDocumenter("fake_package.module.PublicClass")
    assert normalize(str(documenter)) == normalize(
        """
        .. autoclass:: PublicClass
           :members:
           :undoc-members:
        """
    )


def test_str_02(test_path):
    documenter = uqbar.apis.ClassDocumenter("fake_package.module.ChildClass")
    assert normalize(str(documenter)) == normalize(
        """
        .. autoclass:: ChildClass
           :members:
           :undoc-members:
        """
    )


def test_str_03(test_path):
    documenter = uqbar.apis.ClassDocumenter("fake_package.module._PrivateClass")
    assert normalize(str(documenter)) == normalize(
        """
        .. autoclass:: _PrivateClass
           :members:
           :undoc-members:
        """
    )
