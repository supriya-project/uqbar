import copy
import typing

from uqbar.iterables import nwise


class UniqueTreeNode:
    """
    A node in a "unique" tree.

    Unique tree nodes may have at most one parent and may appear only once in
    the tree.
    """

    ### CLASS VARIABLES ###

    _state_flag_names: typing.Tuple[str, ...] = ()

    ### INITIALIZER ###

    def __init__(self, name: str = None) -> None:
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
