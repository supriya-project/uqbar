def _make_class():
    class MyParentClass:
        pass

    return MyParentClass


MyParentClass = _make_class()


class MyChildClass(MyParentClass):  # type: ignore
    pass
