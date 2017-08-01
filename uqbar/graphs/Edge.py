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
        self._tail = None
        self._is_directed = bool(is_directed)
        self._head_port_position = head_port_position
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
        tail_name = self.tail.canonical_name
        if self._tail_port_position is not None:
            tail_name = '{}:{}'.format(tail_name, self._tail_port_position)
        head_name = self.head.canonical_name
        if self._head_port_position is not None:
            head_name = '{}:{}'.format(head_name, self._head_port_position)
        edge_definition = '{} {} {}'.format(
            self._format_value(tail_name),
            connection,
            self._format_value(head_name),
            )
        result = [edge_definition]
        if len(self.attributes):
            attributes = format(self.attributes, 'graphviz').split('\n')
            result[0] = '{} {}'.format(result[0], attributes[0])
            result.extend(attributes[1:])
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
