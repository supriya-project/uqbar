import copy
from uqbar.containers.UniqueTreeNode import UniqueTreeNode


class UniqueTreeContainer(UniqueTreeNode):
    """
    A container node in a "unique" tree.

    Container nodes may contain zero or more other nodes.

    Unique tree nodes may have at most one parent and may appear only once in
    the tree.
    """

    ### INITIALIZER ###

    def __init__(self, children=None, name=None):
        UniqueTreeNode.__init__(self, name=name)
        self._children = []
        self._named_children = {}
        if children is not None:
            self[:] = children

    ### SPECIAL METHODS ###

    def __contains__(self, expr):
        if isinstance(expr, str):
            return expr in self._named_children
        for x in self._children:
            if x is expr:
                return True
        return False

    def __delitem__(self, i):
        if isinstance(i, str):
            children = tuple(self._named_children[i])
            for child in children:
                parent = child.parent
                del(parent[parent.index(child)])
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
            result = sorted(
                self._named_children[expr],
                key=lambda x: x.graph_order,
                )
            if len(result) == 1:
                return result[0]
            return result
        raise ValueError(expr)

    def __iter__(self):
        for child in self._children:
            yield child

    def __len__(self):
        return len(self._children)

    def __setitem__(self, i, expr):
        if isinstance(i, int):
            expr = self._prepare_setitem_single(expr)
            assert isinstance(expr, self._node_class)
            old = self[i]
            if expr in self.parentage:
                raise ValueError('Cannot set parent node as child.')
            old._set_parent(None)
            expr._set_parent(self)
            self._children.insert(i, expr)
        else:
            expr = self._prepare_setitem_multiple(expr)
            if isinstance(expr, UniqueTreeContainer):
                # Prevent mutating while iterating by copying.
                expr = expr[:]
            assert all(isinstance(x, self._node_class) for x in expr)
            if i.start == i.stop and i.start is not None \
                and i.stop is not None and i.start <= -len(self):
                start, stop = 0, 0
            else:
                start, stop, stride = i.indices(len(self))
            old = self[start:stop]
            parentage = self.parentage
            if any(node in parentage for node in expr):
                raise ValueError('Cannot set parent node as child.')
            for node in old:
                node._set_parent(None)
            for node in expr:
                node._set_parent(self)
            self._children.__setitem__(slice(start, start), expr)
        self._mark_entire_tree_for_later_update()

    ### PRIVATE METHODS ###

    def _cache_named_children(self):
        name_dictionary = super(UniqueTreeContainer, self)._cache_named_children()
        if hasattr(self, '_named_children'):
            for name, children in self._named_children.items():
                name_dictionary[name] = copy.copy(children)
        return name_dictionary

    def _prepare_setitem_single(self, expr):
        return expr

    def _prepare_setitem_multiple(self, expr):
        return expr

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self):
        return UniqueTreeNode

    ### PUBLIC METHODS ###

    def append(self, expr):
        self.__setitem__(
            slice(len(self), len(self)),
            [expr]
            )

    def depth_first(self, top_down=True):
        for child in tuple(self):
            if top_down:
                yield child
            if isinstance(child, UniqueTreeContainer):
                yield from child.depth_first(top_down=top_down)
            if not top_down:
                yield child

    def extend(self, expr):
        self.__setitem__(
            slice(len(self), len(self)),
            expr
            )

    def index(self, expr):
        for i, child in enumerate(self._children):
            if child is expr:
                return i
        else:
            message = '{!r} not in {!r}.'
            message = message.format(expr, self)
            raise ValueError(message)

    def insert(self, i, expr):
        self.__setitem__(
            slice(i, i),
            [expr]
            )

    def pop(self, i=-1):
        node = self[i]
        del(self[i])
        return node

    def recurse(self):
        for child in self:
            yield child
            if isinstance(child, type(self)):
                for grandchild in child.recurse():
                    yield grandchild

    def remove(self, node):
        i = self.index(node)
        del(self[i])

    ### PUBLIC PROPERTIES ###

    @property
    def children(self):
        return tuple(self._children)
