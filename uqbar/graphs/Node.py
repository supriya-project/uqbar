from uqbar.containers import UniqueTreeNode
from uqbar.graphs.Attributes import Attributes


class Node(UniqueTreeNode):

    ### INITIALIZER ###

    def __init__(self, name=None, attributes=None):
        UniqueTreeNode.__init__(self, name=name)
        self._attributes = Attributes('edge', **(attributes or {}))

    ### SPECIAL METHODS ###

    def __format__(self, format_spec=None):
        # TODO: make the format specification options machine-readable
        pass

    ### PRIVATE METHODS ###

    def _get_canonical_name(self):
        name_prefix = 'node'
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

    ### PUBLIC PROPERTIES ###

    @property
    def attributes(self):
        return self._attributes
