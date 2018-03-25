from typing import Tuple
from uqbar.containers import UniqueTreeContainer


class TableRow(UniqueTreeContainer):
    """
    A Graphviz HTML table row.

    ::

        >>> import uqbar.graphs
        >>> table_row = uqbar.graphs.TableRow()
        >>> print(format(table_row, 'graphviz'))
        <TR></TR>

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
        result = []
        result.append('<TR>')
        for child in self:
            result.append(format(child, 'graphviz'))
        result.append('</TR>')
        return ''.join(result)

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self) -> Tuple[type, ...]:
        import uqbar.graphs
        return (
            uqbar.graphs.TableCell,
            uqbar.graphs.VRule,
            )
