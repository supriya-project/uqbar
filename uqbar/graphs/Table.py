from typing import Tuple
from uqbar.containers import UniqueTreeContainer


class Table(UniqueTreeContainer):
    """
    A Graphviz HTML table.
    """

    @property
    def _node_class(self) -> Tuple[type, ...]:
        import uqbar.graphs
        return (
            uqbar.graphs.TableRow,
            uqbar.graphs.HRule,
            )
