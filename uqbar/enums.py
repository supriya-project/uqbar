import enum
from uqbar.strings import to_snake_case


class EnumMixin:

    # ### SPECIAL METHODS ### #

    def __dir__(self):
        names = [
            '__class__',
            '__doc__',
            '__format__',
            '__members__',
            '__module__',
            '__repr__',
            'from_expr',
            ]
        names += self._member_names_
        names += [
            ]
        return sorted(names)

    def __repr__(self):
        return '{}.{}'.format(
            type(self).__name__,
            self.name,
            )

    # ### PUBLIC METHODS ### #

    @classmethod
    def from_expr(cls, expr):
        r'''Convenience constructor for enumerations.

        Returns new enumeration item.
        '''
        if isinstance(expr, cls):
            return expr
        elif isinstance(expr, int):
            return cls(expr)
        elif isinstance(expr, str):
            expr = expr.strip()
            expr = to_snake_case(expr)
            expr = expr.upper()
            try:
                return cls[expr]
            except KeyError:
                return cls[expr.replace('_', '')]
        elif expr is None:
            return cls(0)
        message = 'Cannot instantiate {} from {}.'.format(
            cls.__name__,
            expr,
            )
        raise ValueError(message)


class IntEnumeration(EnumMixin, enum.IntEnum):
    """
    Enumeration which behaves like an integer.
    """
    pass


class StrictEnumeration(EnumMixin, enum.Enum):
    """
    Sortable enumeration which does not compare to objects not of its type.
    """

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
