from typing import Iterable, Mapping, Set, Tuple, Union  # noqa

from uqbar.containers import UniqueTreeList

from .Attributes import Attributes
from .Edge import Edge  # noqa
from .RecordField import RecordField
from .RecordGroup import RecordGroup
from .Table import Table


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
        children: Iterable[Union[RecordField, RecordGroup]] = None,
        *,
        attributes: Union[Mapping[str, object], Attributes] = None,
        name: str = None,
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
    ) -> Edge:
        import uqbar.graphs

        edge = uqbar.graphs.Edge(
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
        import uqbar.graphs

        return (uqbar.graphs.RecordField, uqbar.graphs.RecordGroup, uqbar.graphs.Table)

    ### PUBLIC PROPERTIES ###

    @property
    def attributes(self) -> Attributes:
        return self._attributes

    @property
    def edges(self) -> Set[Edge]:
        return set(self._edges)
