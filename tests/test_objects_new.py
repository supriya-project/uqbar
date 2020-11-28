import uqbar.objects
import uqbar.strings


class MyObject:
    def __init__(self, arg1, arg2, *var_args, foo=None, bar=None, **kwargs):
        self.arg1 = arg1
        self.arg2 = arg2
        self.var_args = var_args
        self.foo = foo
        self.bar = bar
        self.kwargs = kwargs

    def __repr__(self):
        return uqbar.objects.get_repr(self)


def test_objects_new_01():
    object_a = MyObject("a", "b", "c", "d", foo="x", quux=["y", "z"])
    object_b = uqbar.objects.new(
        object_a, arg2=MyObject("x", "y", bar=[1, 2, 3]), foo="FOO"
    )
    # object A is unchanged
    assert repr(object_a) == uqbar.strings.normalize(
        """
        MyObject(
            'a',
            'b',
            'c',
            'd',
            foo='x',
            quux=['y', 'z'],
        )
        """
    )
    assert repr(object_b) == uqbar.strings.normalize(
        """
        MyObject(
            'a',
            MyObject(
                'x',
                'y',
                bar=[1, 2, 3],
            ),
            'c',
            'd',
            foo='FOO',
            quux=['y', 'z'],
        )
        """
    )
    object_c = uqbar.objects.new(
        object_b, arg1="new a", arg2__foo="new FOO", arg2__bar=[4, 5, 6, 7]
    )
    # object B is unchanged
    assert repr(object_b) == uqbar.strings.normalize(
        """
        MyObject(
            'a',
            MyObject(
                'x',
                'y',
                bar=[1, 2, 3],
            ),
            'c',
            'd',
            foo='FOO',
            quux=['y', 'z'],
        )
        """
    )
    assert repr(object_c) == uqbar.strings.normalize(
        """
        MyObject(
            'new a',
            MyObject(
                'x',
                'y',
                bar=[4, 5, 6, 7],
                foo='new FOO',
            ),
            'c',
            'd',
            foo='FOO',
            quux=['y', 'z'],
        )
        """
    )
