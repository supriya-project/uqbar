from typing import Tuple
from uqbar.containers import UniqueTreeContainer
from uqbar.graphs import Attachable


class TableCell(UniqueTreeContainer, Attachable):
    """
    A Graphviz HTML table.

    ::

        >>> import uqbar.graphs
        >>> table_cell = uqbar.graphs.TableCell()
        >>> print(format(table_cell, 'graphviz'))
        <TD></TD>

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'HTML Classes'

    ### INITIALIZER ###

    def __init__(
        self,
        children=None,
        *,
        name=None,
        ) -> None:
        from uqbar.graphs import Text
        if isinstance(children, str):
            children = [Text(children)]
        UniqueTreeContainer.__init__(
            self,
            children=children,
            name=name,
            )
        Attachable.__init__(self)

    ### SPECIAL METHODS ###

    def __format__(self, format_spec: str=None) -> str:
        # TODO: make the format specification options machine-readable
        if format_spec == 'graphviz':
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self) -> str:
        result = []
        result.append('<TD>')
        for child in self:
            result.append(format(child, 'graphviz'))
        result.append('</TD>')
        return ''.join(result)

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self) -> Tuple[type, ...]:
        import uqbar.graphs
        return (
            uqbar.graphs.Table,
            uqbar.graphs.LineBreak,
            uqbar.graphs.Text,
            )
