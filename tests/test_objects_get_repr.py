import uqbar.objects
import uqbar.strings


class MyNonReprObject:
    def __init__(self, arg1, arg2, *var_args, foo=None, bar=None, **kwargs):
        self.arg1 = arg1
        self.arg2 = arg2
        self.var_args = var_args
        self.foo = foo
        self.bar = bar
        self.kwargs = kwargs


class MyReprObject(MyNonReprObject):
    def __repr__(self):
        return uqbar.objects.get_repr(self)


def test_objects_get_repr_01():
    my_object = MyNonReprObject("a", "b", "c", "d", foo="x", quux=["y", "z"])
    assert uqbar.objects.get_repr(my_object) == uqbar.strings.normalize(
        """
        MyNonReprObject(
            'a',
            'b',
            'c',
            'd',
            foo='x',
            quux=['y', 'z'],
        )
        """
    )


def test_objects_get_repr_02():
    my_object = MyReprObject("a", "b", "c", "d", foo="x", quux=["y", "z"])
    assert uqbar.objects.get_repr(my_object) == uqbar.strings.normalize(
        """
        MyReprObject(
            'a',
            'b',
            'c',
            'd',
            foo='x',
            quux=['y', 'z'],
        )
        """
    )


def test_objects_get_repr_03():
    my_object = MyReprObject("a", "b", "c", "d", foo="x", quux=["y", "z"])
    assert repr(my_object) == uqbar.strings.normalize(
        """
        MyReprObject(
            'a',
            'b',
            'c',
            'd',
            foo='x',
            quux=['y', 'z'],
        )
        """
    )


def test_objects_get_repr_04():
    object_a = MyReprObject("a", "b", "c", "d", foo="x", quux=["y", "z"])
    object_b = MyReprObject("pqr", object_a, bar=set([1, 2, 3]))
    assert repr(object_b) == uqbar.strings.normalize(
        """
        MyReprObject(
            'pqr',
            MyReprObject(
                'a',
                'b',
                'c',
                'd',
                foo='x',
                quux=['y', 'z'],
            ),
            bar={1, 2, 3},
        )
    """
    )


def test_objects_get_repr_05():
    object_a = MyReprObject("a", "b", "c", "d", foo="x", quux=["y", "z"])
    object_b = MyReprObject("pqr", [object_a], bar=set([1, 2, 3]))
    assert repr(object_b) == uqbar.strings.normalize(
        """
        MyReprObject(
            'pqr',
            [
                MyReprObject(
                    'a',
                    'b',
                    'c',
                    'd',
                    foo='x',
                    quux=['y', 'z'],
                ),
            ],
            bar={1, 2, 3},
        )
    """
    )
