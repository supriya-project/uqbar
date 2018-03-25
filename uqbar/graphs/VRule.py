from uqbar.containers.UniqueTreeNode import UniqueTreeNode


class VRule(UniqueTreeNode):
    """
    A Graphviz HTML vertical rule.

    ::

        >>> import uqbar.graphs
        >>> hrule = uqbar.graphs.VRule()
        >>> print(format(hrule, 'graphviz'))
        <VR/>

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'HTML Classes'

    ### SPECIAL METHODS ###

    def __format__(self, format_spec: str=None) -> str:
        # TODO: make the format specification options machine-readable
        if format_spec == 'graphviz':
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self) -> str:
        return '<VR/>'
