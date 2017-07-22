from uqbar.containers import UniqueTreeContainer
from uqbar.graphs.Attributes import Attributes


class Graph(UniqueTreeContainer):

    ### INITIALIZER ###

    def __init__(
        self,
        name=None,
        children=None,
        is_cluster=None,
        attributes=None,
        edge_attributes=None,
        node_attributes=None,
        ):
        UniqueTreeContainer.__init__(self, name=name, children=children)
        if is_cluster is not None:
            is_cluster = bool(is_cluster)
        mode = 'graph'
        if is_cluster:
            mode = 'cluster'
        self._attributes = Attributes(mode, **(attributes or {}))
        self._edge_attributes = Attributes('edge', **(attributes or {}))
        self._node_attributes = Attributes('node', **(attributes or {}))
        self._is_cluster = is_cluster

    ### SPECIAL METHODS ###

    def __format__(self, format_spec=None):
        # TODO: make the format specification options machine-readable
        pass

    ### PRIVATE METHODS ###

    def _get_canonical_name(self):
        name_prefix = 'graph'
        if self.is_cluster:
            name_prefix = 'cluster'
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

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self):
        import uqbar.graphs
        return (
            uqbar.graphs.Graph,
            uqbar.graphs.Node,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def attributes(self):
        return self._attributes

    @property
    def edge_attributes(self):
        return self._edge_attributes

    @property
    def is_cluster(self):
        return self._is_cluster

    @property
    def node_attributes(self):
        return self._node_attributes
