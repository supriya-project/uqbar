from typing import Dict, List, Mapping, Set, Tuple, Union  # noqa

from uqbar.containers import UniqueTreeList

from .Attributes import Attributes
from .Edge import Edge  # noqa
from .Node import Node  # noqa


class Graph(UniqueTreeList):
    """
    A Graphviz graph, subgraph or cluster.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Core Classes"

    ### INITIALIZER ###

    def __init__(
        self,
        children=None,
        *,
        attributes: Union[Mapping[str, object], Attributes] = None,
        edge_attributes: Union[Mapping[str, object], Attributes] = None,
        is_cluster: bool = False,
        is_digraph: bool = True,
        name: str = None,
        node_attributes: Union[Mapping[str, object], Attributes] = None,
    ) -> None:
        UniqueTreeList.__init__(self, name=name, children=children)
        self._attributes = Attributes(
            "cluster" if is_cluster else "graph", **(attributes or {})
        )
        self._edge_attributes = Attributes("edge", **(edge_attributes or {}))
        self._node_attributes = Attributes("node", **(node_attributes or {}))
        self._is_cluster = bool(is_cluster)
        self._is_digraph = bool(is_digraph)

    ### SPECIAL METHODS ###

    def __format__(self, format_spec: str = None) -> str:
        # TODO: make the format specification options machine-readable
        if format_spec == "graphviz":
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self) -> str:
        def recurse(graph):
            indent = "    "
            result = []
            if not graph.parent:
                name = graph.name or "G"
                if graph.is_digraph:
                    string = "digraph {} {{".format(Attributes._format_value(name))
                else:
                    string = "graph {} {{".format(Attributes._format_value(name))
            else:
                if graph.name is not None:
                    name = graph.name
                    if graph.is_cluster:
                        name = "cluster_{}".format(name)
                else:
                    name = graph._get_canonical_name()
                string = "subgraph {} {{".format(Attributes._format_value(name))
            result.append(string)
            if graph.attributes:
                attributes = "graph {}".format(
                    format(graph.attributes, "graphviz")
                ).split("\n")
                result.extend(indent + line for line in attributes)
            if graph.node_attributes:
                attributes = "node {}".format(
                    format(graph.node_attributes, "graphviz")
                ).split("\n")
                result.extend(indent + line for line in attributes)
            if graph.edge_attributes:
                attributes = "edge {}".format(
                    format(graph.edge_attributes, "graphviz")
                ).split("\n")
                result.extend(indent + line for line in attributes)
            for child in graph:
                if isinstance(child, type(self)):
                    lines = (indent + line for line in recurse(child))
                else:
                    lines = (
                        indent + line for line in format(child, "graphviz").split("\n")
                    )
                result.extend(lines)
            if graph in edge_parents:
                for edge in edge_parents[graph]:
                    lines = format(edge, "graphviz").split("\n")
                    result.extend(indent + line for line in lines)
            result.append("}")
            return result

        all_edges: Set[Edge] = set()
        for child in self.depth_first():
            for edge in getattr(child, "edges", ()):
                if edge.tail.root is not edge.head.root:
                    continue
                all_edges.add(edge)
        edge_parents: Dict[Graph, List[Edge]] = {}
        for edge in sorted(
            all_edges, key=lambda edge: (edge.tail_graph_order, edge.head_graph_order)
        ):
            highest_parent = edge._get_highest_parent()
            edge_parents.setdefault(highest_parent, []).append(edge)

        return "\n".join(recurse(self))

    ### PRIVATE METHODS ###

    def _get_canonical_name(self) -> str:
        name_prefix = "graph"
        if self.is_cluster:
            name_prefix = "cluster"
        if self.name is not None:
            name = self.name
            root = self.root
            if root:
                instances = root[self.name]
                if not isinstance(instances, type(self)):
                    name = "{}_{}".format(name, instances.index(self))
            suffix = name
        elif self.graph_order:
            suffix = "_".join(str(x) for x in self.graph_order)
        else:
            suffix = "0"
        return "{}_{}".format(name_prefix, suffix)

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self) -> Tuple[type, ...]:
        import uqbar.graphs

        return (uqbar.graphs.Graph, uqbar.graphs.Node)

    ### PUBLIC PROPERTIES ###

    @property
    def attributes(self) -> Attributes:
        return self._attributes

    @property
    def edge_attributes(self) -> Attributes:
        return self._edge_attributes

    @property
    def is_cluster(self) -> bool:
        return self._is_cluster

    @property
    def is_digraph(self) -> bool:
        return self._is_digraph

    @property
    def node_attributes(self) -> Attributes:
        return self._node_attributes
