from uqbar.graphs.Attributes import Attributes


class Edge(object):

    ### INITIALIZER ###

    def __init__(
        self,
        attributes=None,
        is_directed=True,
        head_port_position=None,
        tail_port_position=None,
        ):
        self._attributes = Attributes('edge', **(attributes or {}))
        self._head = None
        self._head_port_position = head_port_position
        self._is_directed = bool(is_directed)
        self._tail = None
        self._tail_port_position = tail_port_position

    ### SPECIAL METHODS ###

    def __format__(self, format_spec=None):
        # TODO: make the format specification options machine-readable
        if format_spec == 'graphviz':
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self):
        connection = '->'
        if not self.is_directed:
            connection = '--'
        tail_name = self.tail._get_canonical_name()
        if self._tail_port_position is not None:
            tail_name = '{}:{}'.format(tail_name, self._tail_port_position)
        head_name = self.head._get_canonical_name()
        if self._head_port_position is not None:
            head_name = '{}:{}'.format(head_name, self._head_port_position)
        edge_definition = '{} {} {}'.format(
            Attributes._format_value(tail_name),
            connection,
            Attributes._format_value(head_name),
            )
        result = [edge_definition]
        if len(self.attributes):
            attributes = format(self.attributes, 'graphviz').split('\n')
            result[0] = '{} {}'.format(result[0], attributes[0])
            result.extend(attributes[1:])
        else:
            result[-1] += ';'
        return '\n'.join(result)

    ### PRIVATE METHODS ###

    def _get_highest_parent(self):
        highest_parent = None
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

    def attach(self, tail, head):
        from uqbar.graphs import Node
        prototype = (Node,)
        assert isinstance(tail, prototype)
        assert isinstance(head, prototype)
        self.detach()
        tail._edges.add(self)
        head._edges.add(self)
        self._tail = tail
        self._head = head
        return self

    def detach(self):
        if self.tail is not None:
            self.tail._edges.remove(self)
            self._tail = None
        if self.head is not None:
            self.head._edges.remove(self)
            self._head = None
        return self

    ### PUBLIC PROPERTIES ###

    @property
    def attributes(self):
        return self._attributes

    @property
    def head(self):
        return self._head

    @property
    def head_port_position(self):
        return self._head_port_position

    @property
    def is_directed(self):
        return self._is_directed

    @property
    def tail(self):
        return self._tail

    @property
    def tail_port_position(self):
        return self._tail_port_position
