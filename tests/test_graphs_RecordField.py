from uqbar.graphs import Graph, Node, RecordField, RecordGroup
from uqbar.strings import normalize


def test_graphs_RecordField():

    graph = Graph()
    graph.node_attributes["shape"] = "record"

    node_1_field_0 = RecordField(label="left")
    node_1_field_1 = RecordField(label="middle")
    node_1_field_2 = RecordField(label="right")

    node_1 = Node()
    node_1.extend([node_1_field_0, node_1_field_1, node_1_field_2])

    node_2_field_0 = RecordField(label="one")
    node_2_field_1 = RecordField(label="two")

    node_2 = Node()
    node_2.extend([node_2_field_0, node_2_field_1])

    node_3_field_hello = RecordField(label="hello")
    node_3_field_b = RecordField(label="b")
    node_3_field_c = RecordField(label="c")
    node_3_field_d = RecordField(label="d")
    node_3_field_e = RecordField(label="e")
    node_3_field_f = RecordField(label="f")
    node_3_field_g = RecordField(label="g")
    node_3_field_h = RecordField(label="h")

    inner_group = RecordGroup()
    inner_group.extend([node_3_field_c, node_3_field_d, node_3_field_e])

    outer_group = RecordGroup()
    outer_group.extend([node_3_field_b, inner_group, node_3_field_f])

    node_3 = Node()
    node_3.extend([node_3_field_hello, outer_group, node_3_field_g, node_3_field_h])

    graph.extend([node_1, node_2, node_3])

    node_1_field_1.attach(node_2_field_0)
    node_1_field_2.attach(node_3_field_d)

    graphviz_format = format(graph, "graphviz")

    assert graphviz_format == normalize(
        """
        digraph G {
            node [shape=record];
            node_0 [label="<f_0> left | <f_1> middle | <f_2> right"];
            node_1 [label="<f_0> one | <f_1> two"];
            node_2 [label="<f_0> hello | { <f_1_0> b | { <f_1_1_0> c | <f_1_1_1> d | <f_1_1_2> e } | <f_1_2> f } | <f_2> g | <f_3> h"];
            node_0:f_1 -> node_1:f_0;
            node_0:f_2 -> node_2:f_1_1_1;
        }
        """
    )
