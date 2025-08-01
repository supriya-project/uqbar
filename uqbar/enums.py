import enum
from typing import SupportsInt, Type, TypeVar

from .strings import to_snake_case

E = TypeVar("E", bound=enum.IntEnum)


def from_expr(cls: Type[E], expr: E | SupportsInt | str | None) -> E:
    if isinstance(expr, cls):
        return expr
    elif isinstance(expr, SupportsInt):
        return cls(int(expr))
    elif isinstance(expr, str):
        coerced_expr = to_snake_case(expr.strip()).upper()
        try:
            return cls[coerced_expr]
        except KeyError:
            pass
        try:
            return cls[coerced_expr.title()]
        except KeyError:
            pass
        try:
            return cls[coerced_expr.replace("_", "")]
        except KeyError:
            pass
    elif expr is None:
        return cls(0)
    message = "Cannot instantiate {} from {!r}.".format(cls.__name__, expr)
    raise ValueError(message)


class IntEnumeration(enum.IntEnum):
    """
    Enumeration which behaves like an integer.

    ::

        >>> import uqbar.enums
        >>> class MyEnum(uqbar.enums.IntEnumeration):
        ...     FOO = -1
        ...     BAR = 0
        ...     BAZ = 1
        ...     QUUX = 2

    ::

        >>> MyEnum.FOO < MyEnum.BAR
        True

    Does compare to similarly-valued objects:

    ::

        >>> MyEnum.BAR == False
        True

    """

    pass

    # ### SPECIAL METHODS ### #

    def __dir__(self):
        names = [
            "__class__",
            "__doc__",
            "__format__",
            "__members__",
            "__module__",
            "__repr__",
            "from_expr",
        ]
        names += self._member_names_
        names += []
        return sorted(names)

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self.name)

    # ### PUBLIC METHODS ### #

    @classmethod
    def from_expr(cls, expr):
        """
        Convenience constructor for enumerations.

        ::

            >>> import uqbar.enums
            >>> class MyEnum(uqbar.enums.IntEnumeration):
            ...     A_B = -1
            ...     B_C_D = 0
            ...     E = 1

        ::

            >>> MyEnum.from_expr("a b")
            MyEnum.A_B

        ::

            >>> MyEnum.from_expr(None)
            MyEnum.B_C_D

        ::

            >>> MyEnum.from_expr(1)
            MyEnum.E

        Returns new enumeration item.
        """
        return from_expr(cls, expr)


class StrictEnumeration(enum.Enum):
    """
    Sortable enumeration which does not compare to objects not of its type.

    ::

        >>> import uqbar.enums
        >>> class MyEnum(uqbar.enums.StrictEnumeration):
        ...     FOO = -1
        ...     BAR = 0
        ...     BAZ = 1
        ...     QUUX = 2

    ::

        >>> MyEnum.FOO < MyEnum.BAR
        True

    Does not compare to similarly-valued objects:

    ::

        >>> MyEnum.BAR == False
        False

    """

    # ### SPECIAL METHODS ### #

    def __dir__(self):
        names = [
            "__class__",
            "__doc__",
            "__format__",
            "__members__",
            "__module__",
            "__repr__",
            "from_expr",
        ]
        names += self._member_names_
        names += []
        return sorted(names)

    def __float__(self):
        return float(self.value)

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __int__(self):
        return int(self.value)

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self.name)

    # ### PUBLIC METHODS ### #

    @classmethod
    def from_expr(cls, expr):
        """
        Convenience constructor for enumerations.

        ::

            >>> import uqbar.enums
            >>> class MyEnum(uqbar.enums.StrictEnumeration):
            ...     A_B = -1
            ...     B_C_D = 0
            ...     E = 1

        ::

            >>> MyEnum.from_expr("a b")
            MyEnum.A_B

        ::

            >>> MyEnum.from_expr(None)
            MyEnum.B_C_D

        ::

            >>> MyEnum.from_expr(1)
            MyEnum.E

        Returns new enumeration item.
        """
        return from_expr(cls, expr)
