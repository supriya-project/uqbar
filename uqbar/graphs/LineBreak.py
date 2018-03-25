from uqbar.containers.UniqueTreeNode import UniqueTreeNode


class LineBreak(UniqueTreeNode):
    """
    A Graphviz HTML line break.

    ::

        >>> import uqbar.graphs
        >>> line_break = uqbar.graphs.LineBreak()
        >>> print(format(line_break, 'graphviz'))
        <BR/>

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
        return '<BR/>'
