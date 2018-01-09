from uqbar.containers import UniqueTreeNode


class RecordField(UniqueTreeNode):
    """
    A Graphviz record field.

    ::

        >>> import uqbar.graphs
        >>> field = uqbar.graphs.RecordField()
        >>> print(format(field, 'graphviz'))

    """

    ### INITIALIZER ###

    def __init__(self, *, name=None):
        UniqueTreeNode.__init__(self, name=name)
        self._edges = set()

    ### SPECIAL METHODS ###

    def __format__(self, format_spec=None):
        # TODO: make the format specification options machine-readable
        if format_spec == 'graphviz':
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self):
        result = []
        return '\n'.join(result)

    ### PUBLIC METHODS ###

    def attach(
        self,
        target,
        is_directed=True,
        head_port_position=None,
        tail_port_position=None,
        **attributes
        ):
        import uqbar.graphs
        edge = uqbar.graphs.Edge(
            attributes=attributes,
            head_port_position=head_port_position,
            is_directed=is_directed,
            tail_port_position=tail_port_position,
            )
        edge.attach(self, target)
        return edge

    ### PUBLIC PROPERTIES ###

    @property
    def edges(self):
        return set(self._edges)

    @property
    def node(self):
        from uqbar.graphs import Node
        for parent in self.parentage:
            if isinstance(parent, Node):
                return parent
        return None
