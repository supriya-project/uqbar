import threading

from .UniqueTreeContainer import UniqueTreeContainer


class UniqueTreeSet(UniqueTreeContainer):
    """
    A set-like node in a "unique" tree.
    """

    ### INITIALIZER ###

    def __init__(self, children=None, name=None):
        super().__init__(name=name)
        self._children = set()
        self._lock = threading.RLock()
        if children is not None:
            self.update(children)

    ### PRIVATE METHODS ###

    def _mutate(self, new_nodes, old_nodes):
        with self._lock:
            self._validate(new_nodes, old_nodes)
            self._update_parentage(new_nodes, old_nodes)
            self._mark_entire_tree_for_later_update()

    def _update_parentage(self, new_nodes, old_nodes):
        for old_node in old_nodes:
            old_node._set_parent(None)
        for new_node in new_nodes:
            new_node._set_parent(self)
        self._children.update(new_nodes)

    def _validate(self, new_nodes):
        parentage = self.parentage
        for new_node in new_nodes:
            if not isinstance(new_node, self._node_class):
                raise ValueError(f"Expected {self._node_class}, got {type(new_node)}")
            elif new_node in parentage:
                raise ValueError("Cannot set parent node as child.")

    ### PUBLIC METHODS ###

    def add(self, node):
        self._mutate(new_nodes=(node,), old_nodes=())

    def clear(self):
        self._mutate(new_nodes=(), old_nodes=self._children)

    def pop(self):
        with self._lock:
            node = self._children.pop()
            self._mutate(new_nodes=(), old_nodes=(node,))
        return node

    def remove(self, node):
        with self._lock:
            self._children.remove(node)
            self._mutate(new_nodes=(), old_nodes=(node,))

    def update(self, expr):
        with self._lock:
            self._mutate(new_nodes=expr, old_nodes=())
