from uqbar.containers import UniqueTreeContainer


class RecordGroup(UniqueTreeContainer):
    """
    A Graphviz record field group.

    ::

        >>> import uqbar.graphs
        >>> group = uqbar.graphs.RecordGroup()
        >>> group.extend([
        ...     uqbar.graphs.RecordField(),
        ...     uqbar.graphs.RecordGroup([
        ...         uqbar.graphs.RecordField(),
        ...         uqbar.graphs.RecordField(),
        ...         ]),
        ...     uqbar.graphs.RecordField(),
        ...     ])
        >>> print(format(group, 'graphviz'))

    """

    ### INITIALIZER ###

    def __init__(self, children=None, *, name=None):
        UniqueTreeContainer.__init__(self, name=name, children=children)

    ### SPECIAL METHODS ###

    def __format__(self, format_spec=None):
        # TODO: make the format specification options machine-readable
        if format_spec == 'graphviz':
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self):
        result = []
        return '\n'.join(result)

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self):
        import uqbar.graphs
        return (
            uqbar.graphs.RecordField,
            uqbar.graphs.RecordGroup,
            )

    @property
    def node(self):
        from uqbar.graphs import Node
        for parent in self.parentage:
            if isinstance(parent, Node):
                return parent
        return None
