from typing import Dict, Iterable, List, Mapping, Optional, Set, Tuple, Union  # noqa

import uqbar.graphs

from ..containers import UniqueTreeList, UniqueTreeNode
from .attrs import Attributes


class Attachable(UniqueTreeNode):

    ### CLASS VARIABLES ###

    __documentation_section__ = "Mixins"

    ### INITIALIZER ###

    def __init__(self) -> None:
        self._edges: Set["Edge"] = set()

    ### PRIVATE METHODS ###

    def _get_canonical_name(self) -> str:
        node = self._get_node()
        node_name = ""
        if node is not None:
            node_name = node._get_canonical_name()
        port_name = self._get_port_name()
        return "{}:{}".format(node_name, port_name)

    def _get_node(self) -> Optional["Node"]:
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
            graph_order = graph_order[len(node_graph_order) :]
        else:
            graph_order = (0,)
        return "f_" + "_".join(str(x) for x in graph_order)

    ### PUBLIC METHODS ###

    def attach(
        self,
        target,
        is_directed=True,
        head_port_position=None,
        tail_port_position=None,
        **attributes,
    ) -> "Edge":
        edge = Edge(
            attributes=attributes,
            head_port_position=head_port_position,
            is_directed=is_directed,
            tail_port_position=tail_port_position,
        )
        edge.attach(self, target)
        return edge

    ### PUBLIC PROPERTIES ###

    @property
    def edges(self) -> Set["Edge"]:
        return set(self._edges)


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
        attributes: Optional[Union[Mapping[str, object], Attributes]] = None,
        edge_attributes: Optional[Union[Mapping[str, object], Attributes]] = None,
        is_cluster: bool = False,
        is_digraph: bool = True,
        name: Optional[str] = None,
        node_attributes: Optional[Union[Mapping[str, object], Attributes]] = None,
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

    def __format__(self, format_spec: Optional[str] = None) -> str:
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
        return (Graph, Node)

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


class Node(UniqueTreeList):
    """
    A Graphviz node.

    ::

        >>> import uqbar.graphs
        >>> node = uqbar.graphs.Node()
        >>> print(format(node, 'graphviz'))
        node_0;

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Core Classes"

    ### INITIALIZER ###

    def __init__(
        self,
        children: Optional[
            Iterable[Union["uqbar.graphs.RecordField", "uqbar.graphs.RecordGroup"]]
        ] = None,
        *,
        attributes: Optional[Union[Mapping[str, object], Attributes]] = None,
        name: Optional[str] = None,
    ) -> None:
        UniqueTreeList.__init__(self, name=name, children=children)
        self._attributes = Attributes("node", **(attributes or {}))
        self._edges: Set[Edge] = set()

    ### SPECIAL METHODS ###

    def __format__(self, format_spec=None) -> str:
        # TODO: make the format specification options machine-readable
        if format_spec == "graphviz":
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self) -> str:
        from .html import Table  # avoid circular imports

        node_definition = Attributes._format_value(self._get_canonical_name())
        result = [node_definition]
        attributes = self.attributes.copy()
        if len(self):
            if isinstance(self[0], Table):
                label = "<\n{}>".format(format(self[0], "graphviz"))
            else:
                label = " | ".join(format(_, "graphviz") for _ in self)
            attributes["label"] = label
        if len(attributes):
            attributes = format(attributes, "graphviz").split("\n")
            result[0] = "{} {}".format(result[0], attributes[0])
            result.extend(attributes[1:])
        else:
            result[-1] += ";"
        return "\n".join(result)

    ### PRIVATE METHODS ###

    def _get_canonical_name(self) -> str:
        prefix = "node"
        if self.name is not None:
            root = self.root
            if root:
                instances = root[self.name]
                if instances is not self:
                    return "{}_{}".format(self.name, instances.index(self))
            return self.name
        elif self.graph_order:
            suffix = "_".join(str(x) for x in self.graph_order)
        else:
            suffix = "0"
        return "{}_{}".format(prefix, suffix)

    ### PUBLIC METHODS ###

    def attach(
        self,
        node,
        is_directed=True,
        head_port_position=None,
        tail_port_position=None,
        **attributes,
    ) -> "Edge":
        edge = Edge(
            attributes=attributes,
            head_port_position=head_port_position,
            is_directed=is_directed,
            tail_port_position=tail_port_position,
        )
        edge.attach(self, node)
        return edge

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self) -> Tuple[type, ...]:
        from .html import Table  # avoid circular imports
        from .records import RecordField, RecordGroup  # avoid circular imports

        return (RecordField, RecordGroup, Table)

    ### PUBLIC PROPERTIES ###

    @property
    def attributes(self) -> Attributes:
        return self._attributes

    @property
    def edges(self) -> Set["Edge"]:
        return set(self._edges)


class Edge(object):
    """
    A Graphviz edge.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Core Classes"

    ### INITIALIZER ###

    def __init__(
        self,
        attributes: Optional[Union[Mapping[str, object], Attributes]] = None,
        is_directed: bool = True,
        head_port_position: Optional[str] = None,
        tail_port_position: Optional[str] = None,
    ) -> None:
        self._attributes = Attributes("edge", **(attributes or {}))
        self._head: Optional[Union[Node, Attachable]] = None
        self._head_port_position = head_port_position
        self._is_directed = bool(is_directed)
        self._tail: Optional[Union[Node, Attachable]] = None
        self._tail_port_position = tail_port_position

    ### SPECIAL METHODS ###

    def __format__(self, format_spec=None) -> str:
        # TODO: make the format specification options machine-readable
        if format_spec == "graphviz":
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self) -> str:
        connection = "->"
        if not self.is_directed:
            connection = "--"

        tail_parts = []
        tail_node = None
        tail_port_name = None
        if isinstance(self.tail, Node):
            tail_node = self.tail
        elif isinstance(self.tail, Attachable):
            tail_node = self.tail._get_node()
            tail_port_name = self.tail._get_port_name()
        if tail_node is None:
            raise ValueError
        tail_parts.append(tail_node._get_canonical_name())
        if tail_port_name:
            tail_parts.append(tail_port_name)
        if self.tail_port_position:
            tail_parts.append(self.tail_port_position)
        tail_name = ":".join(Attributes._format_value(part) for part in tail_parts)

        head_parts = []
        head_node = None
        head_port_name = None
        if isinstance(self.head, Node):
            head_node = self.head
        elif isinstance(self.head, Attachable):
            head_node = self.head._get_node()
            head_port_name = self.head._get_port_name()
        if head_node is None:
            raise ValueError
        head_parts.append(head_node._get_canonical_name())
        if head_port_name:
            head_parts.append(head_port_name)
        if self.head_port_position:
            head_parts.append(self.head_port_position)
        head_name = ":".join(Attributes._format_value(part) for part in head_parts)

        edge_definition = "{} {} {}".format(tail_name, connection, head_name)
        result = [edge_definition]
        if len(self.attributes):
            attributes = format(self.attributes, "graphviz").split("\n")
            result[0] = "{} {}".format(result[0], attributes[0])
            result.extend(attributes[1:])
        else:
            result[-1] += ";"
        return "\n".join(result)

    ### PRIVATE METHODS ###

    def _get_highest_parent(self) -> Graph:
        if self.tail is None:
            raise ValueError(self.tail)
        elif self.head is None:
            raise ValueError(self.head)
        highest_parent: Optional[Graph] = None
        tail_parentage = list(self.tail.parentage[1:])
        head_parentage = list(self.head.parentage[1:])
        while (
            len(tail_parentage)
            and len(head_parentage)
            and tail_parentage[-1] is head_parentage[-1]
        ):
            highest_parent = tail_parentage[-1]
            tail_parentage.pop()
            head_parentage.pop()
        if highest_parent is None:
            message = "highest parent can not be none."
            raise Exception(message)
        return highest_parent

    ### PUBLIC METHODS ###

    def attach(
        self, tail: Union[Node, Attachable], head: Union[Node, Attachable]
    ) -> "Edge":
        prototype = (Node, Attachable)
        assert isinstance(tail, prototype)
        assert isinstance(head, prototype)
        self.detach()
        tail._edges.add(self)
        head._edges.add(self)
        self._tail = tail
        self._head = head
        return self

    def detach(self) -> "Edge":
        if self.tail is not None:
            self.tail._edges.remove(self)
            self._tail = None
        if self.head is not None:
            self.head._edges.remove(self)
            self._head = None
        return self

    ### PUBLIC PROPERTIES ###

    @property
    def attributes(self) -> Attributes:
        return self._attributes

    @property
    def head(self) -> Optional[Union[Node, Attachable]]:
        return self._head

    @property
    def head_graph_order(self) -> Tuple[int, ...]:
        if self.head is None:
            return ()
        return self.head.graph_order

    @property
    def head_port_position(self) -> Optional[str]:
        return self._head_port_position

    @property
    def is_directed(self) -> bool:
        return self._is_directed

    @property
    def tail(self) -> Optional[Union[Node, Attachable]]:
        return self._tail

    @property
    def tail_graph_order(self) -> Tuple[int, ...]:
        if self.tail is None:
            return ()
        return self.tail.graph_order

    @property
    def tail_port_position(self) -> Optional[str]:
        return self._tail_port_position
