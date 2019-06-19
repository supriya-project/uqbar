from uqbar.containers.UniqueTreeNode import UniqueTreeNode


class UniqueTreeSet(UniqueTreeNode):

    def __init__(self, children=None, name=None):
        UniqueTreeNode.__init__(self, name=name)
        self._children = set()
        self._named_children = {}
        if children is not None:
            self._children.update(children)

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

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self):
        return UniqueTreeNode

    ### PUBLIC METHODS ###

    def add(self, node):
        pass

    def clear(self):
        pass

    def pop(self):
        pass

    def recurse(self):
        for child in self:
            yield child
            if isinstance(child, type(self)):
                for grandchild in child.recurse():
                    yield grandchild

    def remove(self, node):
        pass

    def update(self, expr):
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def children(self):
        return tuple(self._children)
