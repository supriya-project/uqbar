from uqbar.graphs import Graph, LineBreak, Node, Table, TableCell, TableRow, Text
from uqbar.strings import normalize


def test_graphs_Table():
    """
    digraph structs {

        node [shape=plaintext]


        struct1:f1 -> struct2:f0;
        struct1:f2 -> struct3:here;
    }
    """

    graph = Graph()
    graph.node_attributes["shape"] = "plaintext"

    struct_1_table_row_1_cell_1 = TableCell("left")
    struct_1_table_row_1_cell_2 = TableCell("mid dle")
    struct_1_table_row_1_cell_3 = TableCell("right")
    struct_1_table_row_1 = TableRow(
        [
            struct_1_table_row_1_cell_1,
            struct_1_table_row_1_cell_2,
            struct_1_table_row_1_cell_3,
        ]
    )
    struct_1_table = Table(
        [struct_1_table_row_1],
        attributes={"border": 0, "cellborder": 1, "cellspacing": 0},
    )
    struct_1 = Node([struct_1_table])

    struct_2_table_row_1_cell_1 = TableCell("one")
    struct_2_table_row_1_cell_2 = TableCell("two")
    struct_2_table_row_1 = TableRow(
        [struct_2_table_row_1_cell_1, struct_2_table_row_1_cell_2]
    )
    struct_2_table = Table(
        [struct_2_table_row_1],
        attributes={"border": 0, "cellborder": 1, "cellspacing": 0},
    )
    struct_2 = Node([struct_2_table])

    struct_3_table_row_1_cell_1 = TableCell(
        [Text("hello"), LineBreak(), Text("world")], attributes={"rowspan": 3}
    )
    struct_3_table_row_1_cell_2 = TableCell("b", attributes={"colspan": 3})
    struct_3_table_row_1_cell_3 = TableCell("g", attributes={"rowspan": 3})
    struct_3_table_row_1_cell_4 = TableCell("h", attributes={"rowspan": 3})
    struct_3_table_row_1 = TableRow(
        [
            struct_3_table_row_1_cell_1,
            struct_3_table_row_1_cell_2,
            struct_3_table_row_1_cell_3,
            struct_3_table_row_1_cell_4,
        ]
    )

    struct_3_table_row_2_cell_1 = TableCell("c")
    struct_3_table_row_2_cell_2 = TableCell("d")
    struct_3_table_row_2_cell_3 = TableCell("e")
    struct_3_table_row_2 = TableRow(
        [
            struct_3_table_row_2_cell_1,
            struct_3_table_row_2_cell_2,
            struct_3_table_row_2_cell_3,
        ]
    )

    struct_3_table_row_3_cell_1 = TableCell("f", attributes={"colspan": 3})

    struct_3_table_row_3 = TableRow([struct_3_table_row_3_cell_1])

    struct_3_table = Table(
        [struct_3_table_row_1, struct_3_table_row_2, struct_3_table_row_3],
        attributes={"border": 0, "cellborder": 1, "cellspacing": 0, "cellpadding": 4},
    )
    struct_3 = Node([struct_3_table])

    graph.extend([struct_1, struct_2, struct_3])

    struct_1_table_row_1_cell_2.attach(struct_2_table_row_1_cell_1)
    struct_1_table_row_1_cell_3.attach(struct_3_table_row_2_cell_2)

    graphviz_format = format(graph, "graphviz")

    assert graphviz_format == normalize(
        """
        digraph G {
            node [shape=plaintext];
            node_0 [label=<
                <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
                    <TR>
                        <TD>left</TD>
                        <TD PORT="f_0_0_1">mid dle</TD>
                        <TD PORT="f_0_0_2">right</TD>
                    </TR>
                </TABLE>>];
            node_1 [label=<
                <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
                    <TR>
                        <TD PORT="f_0_0_0">one</TD>
                        <TD>two</TD>
                    </TR>
                </TABLE>>];
            node_2 [label=<
                <TABLE BORDER="0" CELLBORDER="1" CELLPADDING="4" CELLSPACING="0">
                    <TR>
                        <TD ROWSPAN="3">hello<BR/>world</TD>
                        <TD COLSPAN="3">b</TD>
                        <TD ROWSPAN="3">g</TD>
                        <TD ROWSPAN="3">h</TD>
                    </TR>
                    <TR>
                        <TD>c</TD>
                        <TD PORT="f_0_1_1">d</TD>
                        <TD>e</TD>
                    </TR>
                    <TR>
                        <TD COLSPAN="3">f</TD>
                    </TR>
                </TABLE>>];
            node_0:f_0_0_1 -> node_1:f_0_0_0;
            node_0:f_0_0_2 -> node_2:f_0_1_1;
        }
        """
    )
