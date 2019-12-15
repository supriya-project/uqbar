Directives
==========

::

    >>> value = 1

..  book::

    >>> value += 1
    >>> value
    2

..  book-import:: fake_package.module:ChildClass

..  book::
    :hide:

    >>> value += 1
    >>> value
    3

::

    >>> value += 1
    >>> value
    4

::

    >>> ChildClass.__name__
    'ChildClass'

..  book::

    >>> 1 / 0
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ZeroDivisionError: integer division or modulo by zero
