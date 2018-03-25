from typing import Tuple
from uqbar.containers import UniqueTreeContainer


class TableRow(UniqueTreeContainer):
    """
    A Graphviz HTML table row.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'HTML Classes'

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self) -> Tuple[type, ...]:
        import uqbar.graphs
        return (
            uqbar.graphs.TableCell,
            uqbar.graphs.VRule,
            )
