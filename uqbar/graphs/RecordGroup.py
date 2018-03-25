from uqbar.containers import UniqueTreeContainer
from typing import Tuple  # noqa


class RecordGroup(UniqueTreeContainer):
    """ A Graphviz record field group.

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
        { <f_0> | { <f_0> | <f_0> } | <f_0> }

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Record Field Classes'

    ### INITIALIZER ###

    def __init__(
        self,
        children=None,
        *,
        name: str=None
        ) -> None:
        UniqueTreeContainer.__init__(self, name=name, children=children)

    ### SPECIAL METHODS ###

    def __format__(self, format_spec=None) -> str:
        # TODO: make the format specification options machine-readable
        if format_spec == 'graphviz':
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self) -> str:
        result = ' | '.join(
            _ for _ in (format(_, 'graphviz') for _ in self) if _
            )
        if result:
            result = '{{ {} }}'.format(result)
        return result

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self) -> Tuple[type, ...]:
        import uqbar.graphs
        return (
            uqbar.graphs.RecordField,
            uqbar.graphs.RecordGroup,
            )
