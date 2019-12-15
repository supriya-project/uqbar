Fake Docs
=========

::

    >>> print("hello, world!");
    >>> print("foo bar baz!");
    >>> print("i'm on my own line too!");

::

    >>> import uqbar.graphs

::

    >>> g = uqbar.graphs.Graph()
    >>> n1 = uqbar.graphs.Node()
    >>> g.append(n1)

::

    >>> for i in range(3):
    ...     n2 = uqbar.graphs.Node()
    ...     g.append(n2)
    ...     e = n1.attach(n2)
    ...     uqbar.graphs.Grapher(g)()
    ...     print(i)
    ...     n1 = n2
    ...

::

    >>> print(format(g, "graphviz"))

.. toctree::

   api
   directives
