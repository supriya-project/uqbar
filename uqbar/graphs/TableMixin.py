from typing import Union


class TableMixin:

    ### CLASS VARIABLES ###

    __documentation_section__ = 'HTML Mixin Classes'

    ### INITIALIZER ###

    def __init__(
        self,
        align: str=None,
        bgcolor: str=None,
        cellpadding: Union[int, float]=None,
        cellspacing: Union[int, float]=None,
        color: str=None,
        fixedsize: bool=None,
        gradientangle: Union[int, float]=None,
        height: Union[int, float]=None,
        href: str=None,
        id: str=None,
        sides: str=None,
        target: str=None,
        title: str=None,
        tooltip: str=None,
        valign: str=None,
        width: Union[int, float]=None,
        ) -> None:
        self.align = align
        self.bgcolor = bgcolor
        self.cellpadding = cellpadding
        self.cellspacing = cellspacing
        self.color = color
        self.fixedsize = fixedsize
        self.gradientangle = gradientangle
        self.height = height
        self.href = href
        self.id = id
        self.sides = sides
        self.target = target
        self.tooltip = tooltip
        self.valign = valign
        self.width = width

    ### PUBLIC PROPERTIES ###
