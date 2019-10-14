from .UniqueTreeContainer import UniqueTreeContainer


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
