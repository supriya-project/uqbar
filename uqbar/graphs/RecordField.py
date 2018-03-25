import uqbar.graphs  # noqa
from uqbar.containers import UniqueTreeNode
from typing import Optional, Set  # noqa


class RecordField(UniqueTreeNode):
    """
    A Graphviz record field.

    ::

        >>> import uqbar.graphs
        >>> field = uqbar.graphs.RecordField(label='My Label')
        >>> print(format(field, 'graphviz'))
        <f_0> My Label

    Port names are generated based on the graph order of the field within its
    parent node:

    ::

        >>> other_field = uqbar.graphs.RecordField(label='Other Label')
        >>> group = uqbar.graphs.RecordGroup()
        >>> node = uqbar.graphs.Node(attributes=dict(shape='Mrecord'))
        >>> cluster = uqbar.graphs.Graph(is_cluster=True)
        >>> graph = uqbar.graphs.Graph()

    ::

        >>> graph.append(cluster)
        >>> cluster.append(node)
        >>> node.append(group)
        >>> group.extend([other_field, field])
        >>> print(format(field, 'graphviz'))
        <f_0_1> My Label

    If a node contains record fields or groups, their format contributions
    override any string label in the node's attributes:

    ::

        >>> print(format(node, 'graphviz'))
        node_0_0 [label="{ <f_0_0> Other Label | <f_0_1> My Label }",
            shape=Mrecord];

    ::

        >>> node.attributes['label'] = 'Foo'
        >>> print(format(node, 'graphviz'))
        node_0_0 [label="{ <f_0_0> Other Label | <f_0_1> My Label }",
            shape=Mrecord];

    ::

        >>> node[:] = []
        >>> print(format(node, 'graphviz'))
        node_0_0 [label=Foo,
            shape=Mrecord];

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Record Field Classes'

    ### INITIALIZER ###

    def __init__(
        self,
        label: str=None,
        *,
        name: str=None
        ) -> None:
        UniqueTreeNode.__init__(self, name=name)
        self._edges: Set[uqbar.graphs.Edge] = set()
        if label is not None:
            label = str(label)
        self._label = label

    ### SPECIAL METHODS ###

    def __format__(self, format_spec: str=None) -> str:
        # TODO: make the format specification options machine-readable
        if format_spec == 'graphviz':
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self) -> str:
        result = '<{}>'.format(self._get_port_name())
        if self.label:
            result = '{} {}'.format(result, self.label)
        return result

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
        from uqbar.graphs.Edge import Edge
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

    @property
    def label(self) -> Optional[str]:
        return self._label
