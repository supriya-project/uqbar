from typing import Optional, Tuple

from ..containers import UniqueTreeList, UniqueTreeNode
from .core import Attachable


class RecordField(Attachable, UniqueTreeNode):
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

    __documentation_section__ = "Record Field Classes"

    ### INITIALIZER ###

    def __init__(
        self, label: Optional[str] = None, *, name: Optional[str] = None
    ) -> None:
        UniqueTreeNode.__init__(self, name=name)
        Attachable.__init__(self)
        if label is not None:
            label = str(label)
        self._label = label

    ### SPECIAL METHODS ###

    def __format__(self, format_spec: Optional[str] = None) -> str:
        # TODO: make the format specification options machine-readable
        if format_spec == "graphviz":
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self) -> str:
        result = "<{}>".format(self._get_port_name())
        if self.label:
            result = "{} {}".format(result, self.label)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def label(self) -> Optional[str]:
        return self._label


class RecordGroup(UniqueTreeList):
    """
    A Graphviz record field group.

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

    __documentation_section__ = "Record Field Classes"

    ### INITIALIZER ###

    def __init__(self, children=None, *, name: Optional[str] = None) -> None:
        UniqueTreeList.__init__(self, name=name, children=children)

    ### SPECIAL METHODS ###

    def __format__(self, format_spec=None) -> str:
        # TODO: make the format specification options machine-readable
        if format_spec == "graphviz":
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self) -> str:
        result = " | ".join(_ for _ in (format(_, "graphviz") for _ in self) if _)
        if result:
            result = "{{ {} }}".format(result)
        return result

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self) -> Tuple[type, ...]:
        import uqbar.graphs

        return (uqbar.graphs.RecordField, uqbar.graphs.RecordGroup)
