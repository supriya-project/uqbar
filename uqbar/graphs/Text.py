from typing import Union
from uqbar.containers.UniqueTreeNode import UniqueTreeNode
from uqbar.graphs.TextMixin import TextMixin


class Text(UniqueTreeNode, TextMixin):
    """
    A Graphviz HTML text element.
    """

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        bold: bool=None,
        font_color: str=None,
        font_face: str=None,
        font_size: Union[int, float]=None,
        italic: bool=None,
        name: str=None,
        overlined: bool=None,
        strikethrough: bool=None,
        subscript: bool=None,
        superscript: bool=None,
        underlined: bool=None,
        ) -> None:
        UniqueTreeNode.__init__(
            self,
            name=name,
            )
        TextMixin.__init__(
            self,
            bold=bold,
            font_color=font_color,
            font_face=font_face,
            font_size=font_size,
            italic=italic,
            overlined=overlined,
            strikethrough=strikethrough,
            underlined=underlined,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def subscript(self):
        return self._subscript

    @subscript.setter
    def subscript(self, subscript):
        if subscript is not None:
            subscript = bool(subscript)
        self._subscript = subscript

    @property
    def superscript(self):
        return self._superscript

    @superscript.setter
    def superscript(self, superscript):
        if superscript is not None:
            superscript = bool(superscript)
        self._superscript = superscript
