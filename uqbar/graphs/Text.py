from uqbar.containers.UniqueTreeNode import UniqueTreeNode


class Text(UniqueTreeNode):
    """
    A Graphviz HTML text node.

    ::

        >>> import uqbar.graphs
        >>> text = uqbar.graphs.Text('text')
        >>> print(format(text, 'graphviz'))
        text

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "HTML Classes"

    ### INITIALIZER ###

    def __init__(self, text, *, name=None):
        UniqueTreeNode.__init__(self, name=name)
        self.text = text

    ### SPECIAL METHODS ###

    def __format__(self, format_spec: str = None) -> str:
        # TODO: make the format specification options machine-readable
        if format_spec == "graphviz":
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self) -> str:
        return self.text

    ### PUBLIC PROPERTIES ###

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        if text is not None:
            text = str(text)
        self._text = text
