import copy

from uqbar.containers.UniqueTreeNode import UniqueTreeNode


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
