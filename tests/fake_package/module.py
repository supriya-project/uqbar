class PublicClass:
    def __str__(self):
        return repr(self)

    def method(self):
        pass

    def other_method(self):
        pass

    def inheritable_method(self):
        pass

    @classmethod
    def class_method(cls):
        pass

    @staticmethod
    def static_method(cls):
        pass

    @property
    def read_only_property(self):
        pass

    @property
    def read_write_property(self):
        pass

    @read_write_property.setter
    def read_write_property(self, expr):
        pass


class ChildClass(PublicClass):
    def inheritable_method(self):
        pass

    def new_method(self):
        pass


class _PrivateClass:
    pass


def public_function():
    pass


def _private_function():
    pass
