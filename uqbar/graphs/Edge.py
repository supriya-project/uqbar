from uqbar.graphs.Attributes import Attributes


class Edge(object):

    ### INITIALIZER ###

    def __init__(self, attributes=None):
        self._attributes = Attributes('edge', **(attributes or {}))

    ### SPECIAL METHODS ###

    def __format__(self, format_spec=None):
        # TODO: make the format specification options machine-readable
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def attributes(self):
        return self._attributes
