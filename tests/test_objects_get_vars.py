import collections
import enum
from typing import Generic, TypeVar

import pytest

import uqbar.objects


class MyObject:
    def __init__(self, arg1, arg2, *var_args, foo=None, bar=None, **kwargs):
        self.arg1 = arg1
        self.arg2 = arg2
        self.var_args = var_args
        self.foo = foo
        self.bar = bar
        self.kwargs = kwargs


class Enumeration(enum.IntEnum):
    FOO = 1
    BAR = 2
    BAZ = 3


T = TypeVar("T")


class MyGeneric(Generic[T]):
    def __init__(self, arg: T) -> None:
        self.arg = arg


@pytest.mark.parametrize(
    "object_, expected",
    [
        (
            MyObject("a", "b", "c", "d", foo="x", quux=["y", "z"]),
            (
                collections.OrderedDict([("arg1", "a"), ("arg2", "b")]),
                ["c", "d"],
                {"bar": None, "foo": "x", "quux": ["y", "z"]},
            ),
        ),
        (Enumeration.BAZ, (collections.OrderedDict([("value", 3)]), [], {})),
        (MyGeneric[int](arg=3), (collections.OrderedDict([("arg", 3)]), [], {})),
    ],
)
def test_objects_get_vars(object_, expected):
    actual = uqbar.objects.get_vars(object_)
    assert actual == expected
