from typing import Tuple, Union
from uqbar.graphs.TableMixin import TableMixin
from uqbar.containers import UniqueTreeContainer


class TableCell(UniqueTreeContainer, TableMixin):
    """
    A Graphviz HTML table.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'HTML Classes'

    ### INITIALIZER ###

    def __init__(
        self,
        children=None,
        *,
        align: str=None,
        balign: str=None,
        bgcolor: str=None,
        border: Union[int, float]=None,
        cellpadding: Union[int, float]=None,
        cellspacing: Union[int, float]=None,
        color: str=None,
        colspan: int=None,
        fixedsize: bool=None,
        gradientangle: Union[int, float]=None,
        height: Union[int, float]=None,
        href: str=None,
        id: str=None,
        name: str=None,
        rowspan: int=None,
        sides: str=None,
        style: str=None,
        target: str=None,
        title: str=None,
        tooltip: str=None,
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

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self) -> Tuple[type, ...]:
        import uqbar.graphs
        return (
            uqbar.graphs.Table,
            uqbar.graphs.LineBreak,
            uqbar.graphs.Text,
            )

    ### PUBLIC PROPERTIES ###
