import uqbar.graphs  # noqa
from typing import Mapping, Union
from uqbar.graphs.Attributes import Attributes


class Edge(object):
    """
    A Graphviz edge.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Core Classes'

    ### INITIALIZER ###

    def __init__(
        self,
        attributes: Union[Mapping[str, object], Attributes]=None,
        is_directed: bool=True,
        head_port_position: str=None,
        tail_port_position: str=None,
        ) -> None:
        self._attributes = Attributes('edge', **(attributes or {}))
        self._head: Union[uqbar.graphs.Node, uqbar.graphs.RecordField] = None
        self._head_port_position = head_port_position
        self._is_directed = bool(is_directed)
        self._tail: Union[uqbar.graphs.Node, uqbar.graphs.RecordField] = None
        self._tail_port_position = tail_port_position

    ### SPECIAL METHODS ###

    def __format__(self, format_spec=None) -> str:
        # TODO: make the format specification options machine-readable
        if format_spec == 'graphviz':
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self) -> str:
        from uqbar.graphs.Node import Node
        connection = '->'
        if not self.is_directed:
            connection = '--'
        if isinstance(self.tail, Node):
            tail_node = self.tail
            tail_port_name = self._tail_port_position
        else:
            tail_node = self.tail._get_node()
            tail_port_name = self.tail._get_port_name()
        tail_name = Attributes._format_value(tail_node._get_canonical_name())
        if tail_port_name:
            tail_name = '{}:{}'.format(
                tail_name,
                Attributes._format_value(tail_port_name),
                )
        if isinstance(self.head, Node):
            head_node = self.head
            head_port_name = self._head_port_position
        else:
            head_node = self.head._get_node()
            head_port_name = self.head._get_port_name()
        head_name = Attributes._format_value(head_node._get_canonical_name())
        if head_port_name:
            head_name = '{}:{}'.format(
                head_name,
                Attributes._format_value(head_port_name),
                )
        edge_definition = '{} {} {}'.format(tail_name, connection, head_name)
        result = [edge_definition]
        if len(self.attributes):
            attributes = format(self.attributes, 'graphviz').split('\n')
            result[0] = '{} {}'.format(result[0], attributes[0])
            result.extend(attributes[1:])
        else:
            result[-1] += ';'
        return '\n'.join(result)

    ### PRIVATE METHODS ###

    def _get_highest_parent(self) -> 'uqbar.graphs.Graph':
        highest_parent: uqbar.graphs.Graph = None
        tail_parentage = list(self.tail.parentage[1:])
        head_parentage = list(self.head.parentage[1:])
        while (
            len(tail_parentage) and
            len(head_parentage) and
            tail_parentage[-1] is head_parentage[-1]
            ):
            highest_parent = tail_parentage[-1]
            tail_parentage.pop()
            head_parentage.pop()
        if highest_parent is None:
            message = 'highest parent can not be none.'
            raise Exception(message)
        return highest_parent

    ### PUBLIC METHODS ###

    def attach(
        self,
        tail: Union['uqbar.graphs.Node', 'uqbar.graphs.RecordField'],
        head: Union['uqbar.graphs.Node', 'uqbar.graphs.RecordField'],
        ) -> 'Edge':
        from uqbar.graphs.Node import Node
        from uqbar.graphs.RecordField import RecordField
        prototype = (Node, RecordField)
        assert isinstance(tail, prototype)
        assert isinstance(head, prototype)
        self.detach()
        tail._edges.add(self)
        head._edges.add(self)
        self._tail = tail
        self._head = head
        return self

    def detach(self) -> 'Edge':
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
    def head(self) -> Union['uqbar.graphs.Node', 'uqbar.graphs.RecordField']:
        return self._head

    @property
    def head_port_position(self) -> str:
        return self._head_port_position

    @property
    def is_directed(self) -> bool:
        return self._is_directed

    @property
    def tail(self) -> Union['uqbar.graphs.Node', 'uqbar.graphs.RecordField']:
        return self._tail

    @property
    def tail_port_position(self) -> str:
        return self._tail_port_position
