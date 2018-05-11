from uqbar.objects import get_object_hash


def test_objects_get_object_hash_01():
    class MyObject:
        def __init__(self, arg1, arg2, *var_args, foo=None, bar=None, **kwargs):
            self.arg1 = arg1
            self.arg2 = arg2
            self.var_args = var_args
            self.foo = foo
            self.bar = bar
            self.kwargs = kwargs

    object_a = MyObject('a', 'b', 'c', 'd', foo='x', quux=['y', 'z'])
    object_b = MyObject('a', 'b', 'c', 'd', foo='x', quux=['y', 'z'])
    object_c = MyObject('x', 'y', bar=set([1, 2, 3]))
    assert get_object_hash(object_a) == get_object_hash(object_b)
    assert get_object_hash(object_a) != get_object_hash(object_c)
    assert get_object_hash(object_b) != get_object_hash(object_c)
