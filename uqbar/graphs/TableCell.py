from typing import Tuple
from uqbar.graphs.Attributes import Attributes
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
        attributes=None,
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
        self._attributes = Attributes('table_cell', **(attributes or {}))

    ### SPECIAL METHODS ###

    def __format__(self, format_spec: str=None) -> str:
        # TODO: make the format specification options machine-readable
        if format_spec == 'graphviz':
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self) -> str:
        result = []
        start, stop = '<TD', '</TD>'
        if self.edges:
            start += ' PORT="{}"'.format(self._get_port_name())
        start += '>'
        result.append(start)
        for child in self:
            result.append(format(child, 'graphviz'))
        result.append(stop)
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
