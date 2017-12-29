from uqbar.containers import UniqueTreeNode
from uqbar.graphs.Attributes import Attributes


class Node(UniqueTreeNode):
    """
    A Graphviz node.
    """

    ### INITIALIZER ###

    def __init__(self, name=None, attributes=None):
        UniqueTreeNode.__init__(self, name=name)
        self._attributes = Attributes('node', **(attributes or {}))
        self._edges = set()

    ### SPECIAL METHODS ###

    def __format__(self, format_spec=None):
        # TODO: make the format specification options machine-readable
        if format_spec == 'graphviz':
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self):
        node_definition = Attributes._format_value(
            self._get_canonical_name())
        result = [node_definition]
        attributes = self.attributes.copy()  # TODO: handle struct child nodes
        if len(attributes):
            attributes = format(attributes, 'graphviz').split('\n')
            result[0] = '{} {}'.format(result[0], attributes[0])
            result.extend(attributes[1:])
        else:
            result[-1] += ';'
        return '\n'.join(result)

    ### PRIVATE METHODS ###

    def _get_canonical_name(self):
        prefix = 'node'
        if self.name is not None:
            root = self.root
            if root:
                instances = root[self.name]
                if instances is not self:
                    return '{}_{}'.format(self.name, instances.index(self))
            return self.name
        elif self.graph_order:
            suffix = '_'.join(str(x) for x in self.graph_order)
        else:
            suffix = '0'
        return '{}_{}'.format(prefix, suffix)

    ### PUBLIC METHODS ###

    def attach(
        self,
        node,
        is_directed=True,
        head_port_position=None,
        tail_port_position=None,
        **attributes
        ):
        import uqbar.graphs
        edge = uqbar.graphs.Edge(
            attributes=attributes,
            head_port_position=head_port_position,
            is_directed=is_directed,
            tail_port_position=tail_port_position,
            )
        edge.attach(self, node)
        return edge

    ### PUBLIC PROPERTIES ###

    @property
    def attributes(self):
        return self._attributes

    @property
    def edges(self):
        return frozenset(self._edges)
