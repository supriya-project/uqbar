from typing import Tuple, Union
from uqbar.containers import UniqueTreeContainer


class Table(UniqueTreeContainer):
    """
    A Graphviz HTML table.

    ::

        >>> import uqbar.graphs
        >>> table = uqbar.graphs.Table([
        ...     uqbar.graphs.TableRow([
        ...         uqbar.graphs.TableCell('Cell One'),
        ...     ]),
        ...     uqbar.graphs.HRule(),
        ...     uqbar.graphs.TableRow([
        ...         uqbar.graphs.TableCell('Cell Two'),
        ...     ]),
        ... ])
        >>> print(format(table, 'graphviz'))
        <TABLE><TR><TD>Cell One</TD></TR><HR/><TR><TD>Cell Two</TD></TR></TABLE>

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
        UniqueTreeContainer.__init__(
            self,
            children=children,
            name=name,
            )

    ### SPECIAL METHODS ###

    def __format__(self, format_spec: str=None) -> str:
        # TODO: make the format specification options machine-readable
        if format_spec == 'graphviz':
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self) -> str:
        result = []
        result.append('<TABLE>')
        for child in self:
            result.append(format(child, 'graphviz'))
        result.append('</TABLE>')
        return ''.join(result)

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self) -> Tuple[type, ...]:
        import uqbar.graphs
        return (
            uqbar.graphs.TableRow,
            uqbar.graphs.HRule,
            )