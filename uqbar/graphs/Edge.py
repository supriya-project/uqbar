from uqbar.graphs.Attributes import Attributes


class Edge(object):

    ### INITIALIZER ###

    def __init__(
        self,
        tail,
        head,
        attributes=None,
        is_directed=True,
        head_port_position=None,
        tail_port_position=None,
        ):
        from uqbar.graphs import Node
        assert isinstance(head, Node)
        assert isinstance(tail, Node)
        self._attributes = Attributes('edge', **(attributes or {}))
        self._head = head
        self._head_port_position = head_port_position
        self._is_directed = bool(is_directed)
        self._tail = tail
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
