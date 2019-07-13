import collections
import threading

from .UniqueTreeContainer import UniqueTreeContainer


class UniqueTreeDict(UniqueTreeContainer):
    """
    A dict-like node in a "unique" tree.
    """

    ### INITIALIZER ###

    def __init__(self, children=None, name=None):
        super().__init__(name=name)
        self._children = collections.OrderedDict()
        self._children_reversed = {}
        self._lock = threading.RLock()
        if children is not None:
            self.update(children)

    ### SPECIAL METHODS ###

    def __contains__(self, key):
        return key in self._children

    def __delitem__(self, key):
        with self._lock:
            self._mutate([], [(key, self._children[key])])

    def __getitem__(self, key):
        return self._children[key]

    def __iter__(self):
        return iter(self._children)

    def __setitem__(self, key, value):
        self._mutate([(key, value)], [])

    ### PRIVATE METHODS ###

    def _mutate(self, new_items, old_items):
        with self._lock:
            self._validate(new_items, old_items)
            new_nodes, old_nodes = self._update_items(new_items, old_items)
            self._update_parentage(new_nodes, old_nodes)
            self._mark_entire_tree_for_later_update()

    def _update_items(self, new_items, old_items):
        new_nodes, old_nodes = set(), set()
        for old_key, old_node in old_items:
            old_nodes.add(old_node)
            self._children.pop(old_key)
            self._children_reversed.pop(old_node)
        for _, new_node in new_items:
            new_nodes.add(new_node)
        for new_key, new_node in new_items:
            if new_key in self._children:
                # pre-existing key
                old_node = self[new_key]
                if old_node not in new_nodes:
                    old_nodes.add(old_node)
                    self._children_reversed.pop(old_node)
            if new_node in self._children_reversed:
                # pre-existing node
                self._children.pop(self._children_reversed[new_node])
            self._children[new_key] = new_node
            self._children_reversed[new_node] = new_key
        return new_nodes, old_nodes

    def _update_parentage(self, new_nodes, old_nodes):
        for old_node in old_nodes:
            old_node._set_parent(None)
        for new_node in new_nodes:
            new_node._set_parent(self)

    def _validate(self, new_items, old_items):
        parentage = self.parentage
        for _, new_node in new_items:
            if not isinstance(new_node, self._node_class):
                raise ValueError(f"Expected {self._node_class}, got {type(new_node)}")
            elif new_node in parentage:
                raise ValueError("Cannot set parent node as child.")

    ### PUBLIC METHODS ###

    def clear(self):
        self._mutate([], list(self.items()))

    def depth_first(self, top_down=True):
        for child in tuple(self.values()):
            if top_down:
                yield child
            if isinstance(child, UniqueTreeContainer):
                yield from child.depth_first(top_down=top_down)
            if not top_down:
                yield child

    def get(self, key, default=None):
        return self._children.get(key, default)

    def items(self):
        return self._children.items()

    def keys(self):
        return self._children.keys()

    def pop(self, *args):
        with self._lock:
            value = self._children.pop(*args)
            self._children[args[0]] = value
            self._mutate([], [(args[0], value)])
            return value

    def recurse(self):
        return self.depth_first()

    def update(*args, **kwargs):
        self, *args = args
        if len(args) > 1:
            raise TypeError(f"update expected at most 1 arguments, got {len(args)}")
        new_items = {}
        if args:
            new_items.update(dict(args[0]))
        new_items.update(**kwargs)
        self._mutate(list(new_items.items()), [])

    def values(self):
        return self._children.values()
