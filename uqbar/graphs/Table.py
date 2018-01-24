from typing import Tuple, Union
from uqbar.containers import UniqueTreeContainer
from uqbar.graphs.TableMixin import TableMixin
from uqbar.graphs.TextMixin import TextMixin


class Table(UniqueTreeContainer, TableMixin, TextMixin):
    """
    A Graphviz HTML table.
    """

    ### INITIALIZER ###

    def __init__(
        self,
        children=None,
        *,
        align: str=None,
        bgcolor: str=None,
        bold: bool=None,
        border: Union[int, float]=None,
        cellborder: Union[int, float]=None,
        cellpadding: Union[int, float]=None,
        cellspacing: Union[int, float]=None,
        color: str=None,
        columns: str=None,
        fixedsize: bool=None,
        font_color: str=None,
        font_face: str=None,
        font_size: Union[int, float]=None,
        gradientangle: Union[int, float]=None,
        height: Union[int, float]=None,
        href: str=None,
        id: str=None,
        italic: bool=None,
        name: str=None,
        overlined: bool=None,
        rows: str=None,
        sides: str=None,
        strikethrough: bool=None,
        style: str=None,
        target: str=None,
        title: str=None,
        tooltip: str=None,
        underlined: bool=None,
        valign: str=None,
        width: Union[int, float]=None,
        ) -> None:
        UniqueTreeContainer.__init__(
            self,
            children=children,
            name=name,
            )
        TableMixin.__init__(
            self,
            align=align,
            bgcolor=bgcolor,
            cellpadding=cellpadding,
            cellspacing=cellspacing,
            color=color,
            fixedsize=fixedsize,
            gradientangle=gradientangle,
            height=height,
            href=href,
            id=id,
            sides=sides,
            target=target,
            title=title,
            tooltip=tooltip,
            valign=valign,
            width=width,
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

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self) -> Tuple[type, ...]:
        import uqbar.graphs
        return (
            uqbar.graphs.TableRow,
            uqbar.graphs.HRule,
            )

    ### PUBLIC PROPERTIES ###
