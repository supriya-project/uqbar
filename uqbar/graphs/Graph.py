from uqbar.unique_trees import UniqueTreeContainer
from uqbar.graphs.Attributes import Attributes
from uqbar.graphs.Node import Node


class Graph(UniqueTreeContainer):

    ### INITIALIZER ###

    def __init__(
        self,
        name=None,
        children=None,
        is_cluster=None,
        is_digraph=True,
        attributes=None,
        edge_attributes=None,
        node_attributes=None,
        ):
        UniqueTreeContainer.__init__(self, name=name, children=children)
        if is_cluster is not None:
            is_cluster = bool(is_cluster)
        mode = 'graph'
        if is_cluster:
            mode = 'cluster'
        self._attributes = Attributes(mode, **(attributes or {}))
        self._edge_attributes = Attributes('edge', **(attributes or {}))
        self._node_attributes = Attributes('node', **(attributes or {}))
        self._is_cluster = is_cluster
        self._is_digraph = bool(is_digraph)

    ### SPECIAL METHODS ###

    def __format__(self, format_spec=None):
        # TODO: make the format specification options machine-readable
        if format_spec == 'graphviz':
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self):
        def recurse(graph):
            indent = '    '
            result = []
            if not graph.parent:
                name = graph.name or 'G'
                if graph.is_digraph:
                    string = 'digraph {} {{'.format(
                        Attributes._format_value(name))
                else:
                    string = 'graph {} {{'.format(
                        Attributes._format_value(name))
            elif graph.is_cluster:
                name = graph.name or graph._get_canonical_name()
                string = 'subgraph {} {{'.format(
                    Attributes._format_value('cluster_{}'.format(name)))
            else:
                name = graph.name or graph._get_canonical_name()
                string = 'subgraph {} {{'.format(
                    Attributes._format_value(name))
            result.append(string)
            if graph.attributes:
                attributes = 'graph {}'.format(
                    format(graph.attributes, 'graphviz')).split('\n')
                result.extend(indent + line for line in attributes)
            if graph.node_attributes:
                attributes = 'node {}'.format(
                    format(graph.node_attributes, 'graphviz')).split('\n')
                result.extend(indent + line for line in attributes)
            if graph.edge_attributes:
                attributes = 'edge {}'.format(
                    format(graph.edge_attributes, 'graphviz')).split('\n')
                result.extend(indent + line for line in attributes)
            for child in graph:
                if isinstance(child, type(self)):
                    lines = (indent + line for line in recurse(child))
                else:
                    lines = (
                        indent + line for line in
                        format(child, 'graphviz').split('\n')
                        )
                result.extend(lines)
            if graph in edge_parents:
                for edge in edge_parents[graph]:
                    lines = format(edge, 'graphviz').split('\n')
                    result.extend(indent + line for line in lines)
            result.append('}')
            return result

        all_edges = set()
        all_nodes = {}
        for node in self.recurse():
            canonical_name = node._get_canonical_name()
            if canonical_name in all_nodes:
                raise ValueError(node.name, canonical_name)
            all_nodes[canonical_name] = node
            if not isinstance(node, Node):
                continue
            for edge in node.edges:
                if edge in all_edges:
                    continue
                elif edge.tail.root is not edge.head.root:
                    continue
                all_edges.add(edge)
        all_edges = sorted(all_edges, key=lambda edge: (
            edge.tail.graph_order, edge.head.graph_order,
            ))
        edge_parents = {}
        for edge in all_edges:
            highest_parent = edge._get_highest_parent()
            edge_parents.setdefault(highest_parent, []).append(edge)

        return '\n'.join(recurse(self))

    ### PRIVATE METHODS ###

    def _get_canonical_name(self):
        name_prefix = 'graph'
        if self.is_cluster:
            name_prefix = 'cluster'
        if self.name is not None:
            name = '{}_{}'.format(name_prefix, self.name)
            root = self.root
            if root:
                instances = root[self.name]
                if not isinstance(instances, type(self)):
                    name = '{}_{}'.format(name, instances.index(self))
            suffix = name
        elif self.graph_order:
            suffix = '_'.join(str(x) for x in self.graph_order)
        else:
            suffix = '0'
        return '{}_{}'.format(name_prefix, suffix)

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self):
        import uqbar.graphs
        return (
            uqbar.graphs.Graph,
            uqbar.graphs.Node,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def attributes(self):
        return self._attributes

    @property
    def edge_attributes(self):
        return self._edge_attributes

    @property
    def is_cluster(self):
        return self._is_cluster

    @property
    def is_digraph(self):
        return self._is_digraph

    @property
    def node_attributes(self):
        return self._node_attributes
