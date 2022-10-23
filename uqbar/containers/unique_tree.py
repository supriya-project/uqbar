import collections
import copy
import threading
import typing
from typing import Optional

from ..iterables import nwise


class UniqueTreeNode:
    """
    A node in a "unique" tree.

    Unique tree nodes may have at most one parent and may appear only once in
    the tree.
    """

    ### CLASS VARIABLES ###

    _state_flag_names: typing.Tuple[str, ...] = ()

    ### INITIALIZER ###

    def __init__(self, name: Optional[str] = None) -> None:
        self._name = name
        self._parent = None

    ### PRIVATE METHODS ###

    def _cache_named_children(self):
        name_dictionary = {}
        if self.name is not None:
            name_dictionary.setdefault(self.name, set()).add(self)
        return name_dictionary

    @classmethod
    def _iterate_nodes(cls, nodes):
        for x in nodes:
            yield x
            if hasattr(x, "_children"):
                for y in cls._iterate_nodes(x):
                    yield y

    def _get_node_state_flags(self):
        state_flags = {}
        for name in self._state_flag_names:
            state_flags[name] = True
            for node in self.parentage:
                if not getattr(node, name):
                    state_flags[name] = False
                    break
        return state_flags

    def _mark_entire_tree_for_later_update(self):
        for node in self.parentage:
            for name in self._state_flag_names:
                setattr(node, name, False)

    def _remove_from_parent(self):
        if self._parent is not None and self in self._parent:
            self._parent._children.remove(self)
        self._parent = None

    def _remove_named_children_from_parentage(self, old_parent, name_dictionary):
        if old_parent is None or not name_dictionary:
            return
        for parent in old_parent.parentage:
            named_children = parent._named_children
            for name in name_dictionary:
                for node in name_dictionary[name]:
                    named_children[name].remove(node)
                if not named_children[name]:
                    del named_children[name]

    def _restore_named_children_to_parentage(self, new_parent, name_dictionary):
        if new_parent is None or not name_dictionary:
            return
        for parent in new_parent.parentage:
            named_children = parent._named_children
            for name in name_dictionary:
                if name in named_children:
                    named_children[name].update(name_dictionary[name])
                else:
                    named_children[name] = copy.copy(name_dictionary[name])

    def _set_parent(self, new_parent):
        old_parent = self._parent
        named_children = self._cache_named_children()
        self._remove_from_parent()
        self._remove_named_children_from_parentage(old_parent, named_children)
        self._parent = new_parent
        self._restore_named_children_to_parentage(new_parent, named_children)
        if new_parent is None:
            self._mark_entire_tree_for_later_update()

    ### PUBLIC PROPERTIES ###

    @property
    def depth(self):
        return len(self.parentage) - 1

    @property
    def graph_order(self):
        """
        Get graph-order tuple for node.

        ::

            >>> from uqbar.containers import UniqueTreeList, UniqueTreeNode
            >>> root_container = UniqueTreeList(name="root")
            >>> outer_container = UniqueTreeList(name="outer")
            >>> inner_container = UniqueTreeList(name="inner")
            >>> node_a = UniqueTreeNode(name="a")
            >>> node_b = UniqueTreeNode(name="b")
            >>> node_c = UniqueTreeNode(name="c")
            >>> node_d = UniqueTreeNode(name="d")
            >>> root_container.extend([node_a, outer_container])
            >>> outer_container.extend([inner_container, node_d])
            >>> inner_container.extend([node_b, node_c])

        ::

            >>> for node in root_container.depth_first():
            ...     print(node.name, node.graph_order)
            ...
            a (0,)
            outer (1,)
            inner (1, 0)
            b (1, 0, 0)
            c (1, 0, 1)
            d (1, 1)

        """
        graph_order = []
        for parent, child in nwise(reversed(self.parentage)):
            try:
                index = parent.index(child)
            except AttributeError:
                index = 0
            graph_order.append(index)
        return tuple(graph_order)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, expr):
        assert isinstance(expr, (str, type(None)))
        old_name = self._name
        for parent in self.parentage[1:]:
            named_children = parent._named_children
            if old_name is not None:
                named_children[old_name].remove(self)
                if not named_children[old_name]:
                    del named_children[old_name]
            if expr is not None:
                if expr not in named_children:
                    named_children[expr] = set([self])
                else:
                    named_children[expr].add(self)
        self._name = expr

    @property
    def parent(self):
        return self._parent

    @property
    def parentage(self):
        parentage = []
        node = self
        while node is not None:
            parentage.append(node)
            node = getattr(node, "parent", None)
        return tuple(parentage)

    @property
    def root(self):
        proper_parentage = self.parentage[1:]
        if not proper_parentage:
            return None
        return proper_parentage[-1]


class UniqueTreeContainer(UniqueTreeNode):

    ### INITIALIZER ###

    def __init__(self, children=None, name=None):
        UniqueTreeNode.__init__(self, name=name)
        self._named_children = {}

    ### SPECIAL METHODS ###

    def __contains__(self, expr):
        if isinstance(expr, str):
            return expr in self._named_children
        for x in self._children:
            if x is expr:
                return True
        return False

    def __iter__(self):
        for child in self._children:
            yield child

    def __len__(self):
        return len(self._children)

    ### PRIVATE METHODS ###

    def _cache_named_children(self):
        name_dictionary = super()._cache_named_children()
        if hasattr(self, "_named_children"):
            for name, children in self._named_children.items():
                name_dictionary[name] = copy.copy(children)
        return name_dictionary

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self):
        return UniqueTreeNode

    ### PUBLIC METHODS ###

    def depth_first(self, top_down=True, prototype=None):
        for child in tuple(self):
            if top_down:
                if not prototype or isinstance(child, prototype):
                    yield child
            if isinstance(child, UniqueTreeContainer):
                yield from child.depth_first(top_down=top_down, prototype=prototype)
            if not top_down:
                if not prototype or isinstance(child, prototype):
                    yield child

    def recurse(self, prototype=None):
        return self.depth_first(prototype=prototype)

    ### PUBLIC PROPERTIES ###

    @property
    def children(self):
        return tuple(self._children)


class UniqueTreeList(UniqueTreeContainer):
    """
    A list-like node in a "unique" tree.

    List nodes may contain zero or more other nodes.

    Unique tree nodes may have at most one parent and may appear only once in
    the tree.
    """

    ### INITIALIZER ###

    def __init__(self, children=None, name=None):
        super().__init__(name=name)
        self._children = []
        if children is not None:
            self[:] = children

    ### SPECIAL METHODS ###

    def __delitem__(self, i):
        if isinstance(i, str):
            children = tuple(self._named_children[i])
            for child in children:
                parent = child.parent
                del parent[parent.index(child)]
            return
        if isinstance(i, int):
            if i < 0:
                i = len(self) + i
            i = slice(i, i + 1)
        self.__setitem__(i, [])
        self._mark_entire_tree_for_later_update()

    def __getitem__(self, expr):
        if isinstance(expr, (int, slice)):
            return self._children[expr]
        elif isinstance(expr, str):
            result = sorted(self._named_children[expr], key=lambda x: x.graph_order)
            if len(result) == 1:
                return result[0]
            return result
        raise ValueError(expr)

    def __setitem__(self, i, new_items):
        if isinstance(i, int):
            new_items = self._prepare_setitem_single(new_items)
            start_index, stop_index, _ = slice(i, i + 1).indices(len(self))
        else:
            new_items = self._prepare_setitem_multiple(new_items)
            start_index, stop_index, _ = i.indices(len(self))
        old_items = self[start_index:stop_index]
        self._validate(new_items, old_items, start_index, stop_index)
        self._set_items(new_items, old_items, start_index, stop_index)
        self._mark_entire_tree_for_later_update()

    ### PRIVATE METHODS ###

    def _prepare_setitem_multiple(self, expr):
        return list(expr)

    def _prepare_setitem_single(self, expr):
        return [expr]

    def _set_items(self, new_items, old_items, start_index, stop_index):
        for old_item in old_items:
            old_item._set_parent(None)
        for new_item in new_items:
            new_item._set_parent(self)
        self._children.__setitem__(slice(start_index, start_index), new_items)

    def _validate(self, new_nodes, old_nodes, start_index, stop_index):
        parentage = self.parentage
        for new_node in new_nodes:
            if not isinstance(new_node, self._node_class):
                raise ValueError(f"Expected {self._node_class}, got {type(new_node)}")
            elif new_node in parentage:
                raise ValueError("Cannot set parent node as child.")

    ### PUBLIC METHODS ###

    def append(self, expr):
        self.__setitem__(slice(len(self), len(self)), [expr])

    def extend(self, expr):
        self.__setitem__(slice(len(self), len(self)), expr)

    def index(self, expr):
        for i, child in enumerate(self._children):
            if child is expr:
                return i
        message = "{!r} not in {!r}."
        message = message.format(expr, self)
        raise ValueError(message)

    def insert(self, i, expr):
        self.__setitem__(slice(i, i), [expr])

    def pop(self, i=-1):
        node = self[i]
        del self[i]
        return node

    def remove(self, node):
        i = self.index(node)
        del self[i]


class UniqueTreeTuple(UniqueTreeContainer):
    """
    A tuple-like node in a "unique" tree.
    """

    ### INITIALIZER ###

    def __init__(self, children=None, name=None):
        super().__init__(name=name)
        self._children = []
        self._mutate(slice(None), children or ())

    ### SPECIAL METHODS ###

    def __getitem__(self, expr):
        if isinstance(expr, (int, slice)):
            return self._children[expr]
        elif isinstance(expr, str):
            result = sorted(self._named_children[expr], key=lambda x: x.graph_order)
            if len(result) == 1:
                return result[0]
            return result
        raise ValueError(expr)

    ### PRIVATE METHODS ###

    def _mutate(self, i, new_items):
        if isinstance(i, int):
            new_items = self._prepare_setitem_single(new_items)
            start_index, stop_index, _ = slice(i, i + 1).indices(len(self))
        else:
            new_items = self._prepare_setitem_multiple(new_items)
            start_index, stop_index, _ = i.indices(len(self))
        old_items = self[start_index:stop_index]
        self._validate(new_items, old_items, start_index, stop_index)
        self._set_items(new_items, old_items, start_index, stop_index)
        self._mark_entire_tree_for_later_update()

    def _prepare_setitem_multiple(self, expr):
        return list(expr)

    def _prepare_setitem_single(self, expr):
        return [expr]

    def _set_items(self, new_items, old_items, start_index, stop_index):
        for old_item in old_items:
            old_item._set_parent(None)
        for new_item in new_items:
            new_item._set_parent(self)
        self._children.__setitem__(slice(start_index, start_index), new_items)

    def _validate(self, new_nodes, old_nodes, start_index, stop_index):
        parentage = self.parentage
        for new_node in new_nodes:
            if not isinstance(new_node, self._node_class):
                raise ValueError(f"Expected {self._node_class}, got {type(new_node)}")
            elif new_node in parentage:
                raise ValueError("Cannot set parent node as child.")

    ### PUBLIC METHODS ###

    def index(self, expr):
        for i, child in enumerate(self._children):
            if child is expr:
                return i
        message = "{!r} not in {!r}."
        message = message.format(expr, self)
        raise ValueError(message)


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
