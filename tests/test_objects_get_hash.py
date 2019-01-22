from uqbar.objects import get_hash


class MyObject:
    def __init__(self, arg1, arg2, *var_args, foo=None, bar=None, **kwargs):
        self.arg1 = arg1
        self.arg2 = arg2
        self.var_args = var_args
        self.foo = foo
        self.bar = bar
        self.kwargs = kwargs


def test_objects_get_hash_01():
    object_a = MyObject("a", "b", "c", "d", foo="x", quux=["y", "z"])
    object_b = MyObject("a", "b", "c", "d", foo="x", quux=["y", "z"])
    object_c = MyObject("x", "y", bar=set([1, 2, 3]))
    assert get_hash(object_a) == get_hash(object_b)
    assert get_hash(object_a) != get_hash(object_c)
    assert get_hash(object_b) != get_hash(object_c)
