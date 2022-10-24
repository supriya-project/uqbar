from typing import Mapping, Optional, Tuple, Union

from ..containers import UniqueTreeList, UniqueTreeNode
from .attrs import Attributes
from .core import Attachable


class HRule(UniqueTreeNode):
    """
    A Graphviz HTML horizontal rule.

    ::

        >>> import uqbar.graphs
        >>> hrule = uqbar.graphs.HRule()
        >>> print(format(hrule, 'graphviz'))
        <HR/>

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "HTML Classes"

    ### SPECIAL METHODS ###

    def __format__(self, format_spec: Optional[str] = None) -> str:
        # TODO: make the format specification options machine-readable
        if format_spec == "graphviz":
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self) -> str:
        return "<HR/>"


class LineBreak(UniqueTreeNode):
    """
    A Graphviz HTML line break.

    ::

        >>> import uqbar.graphs
        >>> line_break = uqbar.graphs.LineBreak()
        >>> print(format(line_break, 'graphviz'))
        <BR/>

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "HTML Classes"

    ### SPECIAL METHODS ###

    def __format__(self, format_spec: Optional[str] = None) -> str:
        # TODO: make the format specification options machine-readable
        if format_spec == "graphviz":
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self) -> str:
        return "<BR/>"


class Table(UniqueTreeList):
    """
    A Graphviz HTML table.

    ::

        >>> import uqbar.graphs
        >>> table = uqbar.graphs.Table([
        ...     uqbar.graphs.TableRow([
        ...         uqbar.graphs.TableCell('Cell One'),
        ...     ]),
        ...     uqbar.graphs.HRule(),
        ...     uqbar.graphs.TableRow([
        ...         uqbar.graphs.TableCell('Cell Two'),
        ...     ]),
        ... ])
        >>> print(format(table, 'graphviz'))
        <TABLE>
            <TR>
                <TD>Cell One</TD>
            </TR>
            <HR/>
            <TR>
                <TD>Cell Two</TD>
            </TR>
        </TABLE>

    ::

        >>> table = uqbar.graphs.Table(
        ...     attributes={
        ...         'border': 5,
        ...         'bgcolor': 'blue',
        ...         },
        ...     )
        >>> print(format(table, 'graphviz'))
        <TABLE BGCOLOR="blue" BORDER="5"></TABLE>

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "HTML Classes"

    ### INITIALIZER ###

    def __init__(
        self,
        children=None,
        *,
        attributes: Optional[Union[Mapping[str, object], Attributes]] = None,
        name: Optional[str] = None,
    ) -> None:
        UniqueTreeList.__init__(self, children=children, name=name)
        self._attributes = Attributes("table", **(attributes or {}))

    ### SPECIAL METHODS ###

    def __format__(self, format_spec: Optional[str] = None) -> str:
        # TODO: make the format specification options machine-readable
        if format_spec == "graphviz":
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self) -> str:
        result = []
        start, stop = "<TABLE", "</TABLE>"
        attributes = format(self._attributes, "html")
        if attributes:
            start += " {}".format(attributes)
        start += ">"
        result.append(start)
        for child in self:
            for line in format(child, "graphviz").splitlines():
                result.append("    {}".format(line))
        result.append(stop)
        join_character = ""
        if len(result) > 2:
            join_character = "\n"
        return join_character.join(result)

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self) -> Tuple[type, ...]:
        import uqbar.graphs

        return (uqbar.graphs.TableRow, uqbar.graphs.HRule)


class TableRow(UniqueTreeList):
    """
    A Graphviz HTML table row.

    ::

        >>> import uqbar.graphs
        >>> table_row = uqbar.graphs.TableRow()
        >>> print(format(table_row, 'graphviz'))
        <TR></TR>

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "HTML Classes"

    ### SPECIAL METHODS ###

    def __format__(self, format_spec: Optional[str] = None) -> str:
        # TODO: make the format specification options machine-readable
        if format_spec == "graphviz":
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self) -> str:
        result = []
        result.append("<TR>")
        for child in self:
            for line in format(child, "graphviz").splitlines():
                result.append("    {}".format(line))
        result.append("</TR>")
        join_character = ""
        if len(result) > 2:
            join_character = "\n"
        return join_character.join(result)

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self) -> Tuple[type, ...]:
        import uqbar.graphs

        return (uqbar.graphs.TableCell, uqbar.graphs.VRule)


class TableCell(UniqueTreeList, Attachable):
    """
    A Graphviz HTML table.

    ::

        >>> import uqbar.graphs
        >>> table_cell = uqbar.graphs.TableCell()
        >>> print(format(table_cell, 'graphviz'))
        <TD></TD>

    ::

        >>> table_cell = uqbar.graphs.TableCell(
        ...     attributes={
        ...         'border': 5,
        ...         'bgcolor': 'blue',
        ...         },
        ...     )
        >>> print(format(table_cell, 'graphviz'))
        <TD BGCOLOR="blue" BORDER="5"></TD>

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "HTML Classes"

    ### INITIALIZER ###

    def __init__(
        self,
        children=None,
        *,
        attributes: Optional[Union[Mapping[str, object], Attributes]] = None,
        name: Optional[str] = None,
    ) -> None:
        if isinstance(children, str):
            children = [Text(children)]
        UniqueTreeList.__init__(self, children=children, name=name)
        Attachable.__init__(self)
        self._attributes = Attributes("table_cell", **(attributes or {}))

    ### SPECIAL METHODS ###

    def __format__(self, format_spec: Optional[str] = None) -> str:
        # TODO: make the format specification options machine-readable
        if format_spec == "graphviz":
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self) -> str:
        result = []
        start, stop = "<TD", "</TD>"
        if self.edges:
            start += ' PORT="{}"'.format(self._get_port_name())
        attributes = format(self._attributes, "html")
        if attributes:
            start += " {}".format(attributes)
        start += ">"
        result.append(start)
        for child in self:
            result.append(format(child, "graphviz"))
        result.append(stop)
        return "".join(result)

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self) -> Tuple[type, ...]:
        import uqbar.graphs

        return (uqbar.graphs.Table, uqbar.graphs.LineBreak, uqbar.graphs.Text)


class Text(UniqueTreeNode):
    """
    A Graphviz HTML text node.

    ::

        >>> import uqbar.graphs
        >>> text = uqbar.graphs.Text('text')
        >>> print(format(text, 'graphviz'))
        text

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "HTML Classes"

    ### INITIALIZER ###

    def __init__(self, text, *, name=None):
        UniqueTreeNode.__init__(self, name=name)
        self.text = text

    ### SPECIAL METHODS ###

    def __format__(self, format_spec: Optional[str] = None) -> str:
        # TODO: make the format specification options machine-readable
        if format_spec == "graphviz":
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self) -> str:
        return self.text

    ### PUBLIC PROPERTIES ###

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        if text is not None:
            text = str(text)
        self._text = text


class VRule(UniqueTreeNode):
    """
    A Graphviz HTML vertical rule.

    ::

        >>> import uqbar.graphs
        >>> hrule = uqbar.graphs.VRule()
        >>> print(format(hrule, 'graphviz'))
        <VR/>

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "HTML Classes"

    ### SPECIAL METHODS ###

    def __format__(self, format_spec: Optional[str] = None) -> str:
        # TODO: make the format specification options machine-readable
        if format_spec == "graphviz":
            return self.__format_graphviz__()
        return str(self)

    def __format_graphviz__(self) -> str:
        return "<VR/>"
