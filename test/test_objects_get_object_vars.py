import collections
import enum
import uqbar.objects


def test_objects_get_object_vars_01():
    class MyObject:
        def __init__(self, arg1, arg2, *var_args, foo=None, bar=None, **kwargs):
            self.arg1 = arg1
            self.arg2 = arg2
            self.var_args = var_args
            self.foo = foo
            self.bar = bar
            self.kwargs = kwargs
    my_object = MyObject('a', 'b', 'c', 'd', foo='x', quux=['y', 'z'])
    assert uqbar.objects.get_object_vars(my_object) == (
        collections.OrderedDict([('arg1', 'a'), ('arg2', 'b')]),
        ['c', 'd'],
        {'foo': 'x', 'bar': None, 'quux': ['y', 'z']},
    )


def test_objects_get_object_vars_02():
    class Enumeration(enum.IntEnum):
        FOO = 1
        BAR = 2
        BAZ = 3
    my_object = Enumeration.BAZ
    assert uqbar.objects.get_object_vars(my_object) == (
        collections.OrderedDict([('value', 3)]),
        [],
        {},
    )
