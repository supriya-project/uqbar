import uqbar.graphs
from uqbar.containers import UniqueTreeNode
from typing import Optional, Set


class Attachable(UniqueTreeNode):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Mixins'

    ### INITIALIZER ###

    def __init__(self):
        self._edges: Set[uqbar.graphs.Edge] = set()

    ### PRIVATE METHODS ###

    def _get_canonical_name(self) -> str:
        node = self._get_node()
        node_name = ''
        if node is not None:
            node_name = node._get_canonical_name()
        port_name = self._get_port_name()
        return '{}:{}'.format(node_name, port_name)

    def _get_node(self) -> Optional['uqbar.graphs.Node']:
        from uqbar.graphs.Node import Node
        parent = self.parent
        while parent is not None:
            if isinstance(parent, Node):
                return parent
            parent = parent.parent
        return None

    def _get_port_name(self) -> str:
        graph_order = self.graph_order
        node = self._get_node()
        if node is not None:
            node_graph_order = node.graph_order
            graph_order = graph_order[len(node_graph_order):]
        else:
            graph_order = (0,)
        return 'f_' + '_'.join(str(x) for x in graph_order)

    ### PUBLIC METHODS ###

    def attach(
        self,
        target,
        is_directed=True,
        head_port_position=None,
        tail_port_position=None,
        **attributes
        ) -> 'uqbar.graphs.Edge':
        edge = uqbar.graphs.Edge(
            attributes=attributes,
            head_port_position=head_port_position,
            is_directed=is_directed,
            tail_port_position=tail_port_position,
            )
        edge.attach(self, target)
        return edge

    ### PUBLIC PROPERTIES ###

    @property
    def edges(self) -> Set['uqbar.graphs.Edge']:
        return set(self._edges)
