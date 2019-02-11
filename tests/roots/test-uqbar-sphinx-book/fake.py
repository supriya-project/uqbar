class GrandParent:
    """
    A grand parent.

    ::

        >>> print("I am a grand parent")

    """

    def one(self):
        """
        Grand parent: one.

        ::

            >>> print("Grand parent: one.")

        """
        pass

    def two(self):
        """
        Grand parent: two.

        ::

            >>> print("Grand parent: two.")

        """
        pass

    def three(self):
        """
        Grand parent: three.

        ::

            >>> print("Grand parent: three.")

        ::

            >>> import uqbar.graphs
            >>> g = uqbar.graphs.Graph()
            >>> n1 = uqbar.graphs.Node()
            >>> n2 = uqbar.graphs.Node()
            >>> g.extend([n1, n2])
            >>> e = n1.attach(n2)

        ::

            >>> print(format(g, "graphviz"))

        ::

            >>> uqbar.graphs.Grapher(g)()  # doctest: +SKIP

        And that, my friends, is a graph.
        """
        pass


class Parent(GrandParent):
    """
    A parent.

    ::

        >>> print("I am a parent")

    """

    def one(self):
        """
        Parent: one.

        ::

            >>> print("Parent: one.")

        """
        pass


class Uncle(GrandParent):
    # I don't have a docstring or any overridden methods.
    pass


class Child(Parent):
    """
    A child.

    ::

        >>> print("I am a child")

    """

    def two(self):
        """
        Child: two.

        ::

            >>> print("Child: two.")

        """
        pass
