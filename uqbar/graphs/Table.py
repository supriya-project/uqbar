from typing import Mapping, Tuple, Union
from uqbar.graphs.Attributes import Attributes
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
        <TABLE>
            <TR>
                <TD>Cell One</TD>
            </TR>
            <HR/>
            <TR>
                <TD>Cell Two</TD>
            </TR>
        </TABLE>

    ::

        >>> table = uqbar.graphs.Table(
        ...     attributes={
        ...         'border': 5,
        ...         'bgcolor': 'blue',
        ...         },
        ...     )
        >>> print(format(table, 'graphviz'))
        <TABLE BGCOLOR="blue" BORDER="5"></TABLE>

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'HTML Classes'

    ### INITIALIZER ###

    def __init__(
        self,
        children=None,
        *,
        attributes: Union[Mapping[str, object], Attributes]=None,
        name: str=None
        ) -> None:
        UniqueTreeContainer.__init__(
            self,
            children=children,
            name=name,
            )
        self._attributes = Attributes('table', **(attributes or {}))

    ### SPECIAL METHODS ###

    def __format__(self, format_spec: str=None) -> str:
        # TODO: make the format specification options machine-readable
        if format_spec == 'graphviz':
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self) -> str:
        result = []
        start, stop = '<TABLE', '</TABLE>'
        attributes = format(self._attributes, 'html')
        if attributes:
            start += ' {}'.format(attributes)
        start += '>'
        result.append(start)
        for child in self:
            for line in format(child, 'graphviz').splitlines():
                result.append('    {}'.format(line))
        result.append(stop)
        join_character = ''
        if len(result) > 2:
            join_character = '\n'
        return join_character.join(result)

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self) -> Tuple[type, ...]:
        import uqbar.graphs
        return (
            uqbar.graphs.TableRow,
            uqbar.graphs.HRule,
            )
