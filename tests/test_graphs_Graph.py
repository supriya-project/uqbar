import unittest

import uqbar.graphs
import uqbar.strings


class TestCase(unittest.TestCase):
    def test_functional(self):
        # instantiate them
        graph = uqbar.graphs.Graph(name="G")
        cluster_0 = uqbar.graphs.Graph(name="0", is_cluster=True)
        cluster_1 = uqbar.graphs.Graph(name="1", is_cluster=True)
        a0 = uqbar.graphs.Node(name="a0")
        a1 = uqbar.graphs.Node(name="a1")
        a2 = uqbar.graphs.Node(name="a2")
        a3 = uqbar.graphs.Node(name="a3")
        b0 = uqbar.graphs.Node(name="b0")
        b1 = uqbar.graphs.Node(name="b1")
        b2 = uqbar.graphs.Node(name="b2")
        b3 = uqbar.graphs.Node(name="b3")
        start = uqbar.graphs.Node(name="start")
        end = uqbar.graphs.Node(name="end")
        # aggregate them
        graph.extend([cluster_0, cluster_1, start, end])
        cluster_0.extend([a0, a1, a2, a3])
        cluster_1.extend([b0, b1, b2, b3])
        # attach them
        start.attach(a0)
        start.attach(b0)
        a0.attach(a1)
        a1.attach(a2)
        a1.attach(b3)
        a2.attach(a3)
        a3.attach(a0)
        a3.attach(end)
        b0.attach(b1)
        b1.attach(b2)
        b2.attach(b3)
        b2.attach(a3)
        b3.attach(end)
        # style them
        cluster_0.attributes["style"] = "filled"
        cluster_0.attributes["color"] = "lightgrey"
        cluster_0.attributes["label"] = "process #1"
        cluster_0.node_attributes["style"] = "filled"
        cluster_0.node_attributes["color"] = "white"
        cluster_1.attributes["color"] = "blue"
        cluster_1.attributes["label"] = "process #2"
        cluster_1.node_attributes["style"] = ("filled", "rounded")
        start.attributes["shape"] = "Mdiamond"
        end.attributes["shape"] = "Msquare"
        # format them
        assert format(graph) == repr(graph)
        assert format(graph, "graphviz") == uqbar.strings.normalize(
            """
            digraph G {
                subgraph cluster_0 {
                    graph [color=lightgrey,
                        label="process #1",
                        style=filled];
                    node [color=white,
                        style=filled];
                    a0;
                    a1;
                    a2;
                    a3;
                    a0 -> a1;
                    a1 -> a2;
                    a2 -> a3;
                    a3 -> a0;
                }
                subgraph cluster_1 {
                    graph [color=blue,
                        label="process #2"];
                    node [style="filled, rounded"];
                    b0;
                    b1;
                    b2;
                    b3;
                    b0 -> b1;
                    b1 -> b2;
                    b2 -> b3;
                }
                start [shape=Mdiamond];
                end [shape=Msquare];
                a1 -> b3;
                a3 -> end;
                b2 -> a3;
                b3 -> end;
                start -> a0;
                start -> b0;
            }
        """
        )

    def test___format___graphviz_01(self):
        graph = uqbar.graphs.Graph(name="G")
        cluster_foo = uqbar.graphs.Graph(name="foo", is_cluster=True)
        subgraph_bar = uqbar.graphs.Graph(name="bar")
        node_a = uqbar.graphs.Node(name="a")
        node_b = uqbar.graphs.Node(name="b")
        node_c = uqbar.graphs.Node(name="c")
        graph.extend([cluster_foo, subgraph_bar, node_a])
        cluster_foo.append(node_b)
        subgraph_bar.append(node_c)
        node_a.attach(node_b)
        node_a.attach(node_c)
        node_b.attach(node_c)
        assert format(graph, "graphviz") == uqbar.strings.normalize(
            """
        digraph G {
            subgraph cluster_foo {
                b;
            }
            subgraph bar {
                c;
            }
            a;
            b -> c;
            a -> b;
            a -> c;
        }
        """
        )
        cluster_foo.append(node_c)
        assert format(graph, "graphviz") == uqbar.strings.normalize(
            """
            digraph G {
                subgraph cluster_foo {
                    b;
                    c;
                    b -> c;
                }
                subgraph bar {
                }
                a;
                a -> b;
                a -> c;
            }
        """
        )
        subgraph_bar.extend([node_a, node_b, node_c])
        assert format(graph, "graphviz") == uqbar.strings.normalize(
            """
            digraph G {
                subgraph cluster_foo {
                }
                subgraph bar {
                    a;
                    b;
                    c;
                    a -> b;
                    a -> c;
                    b -> c;
                }
            }
        """
        )
        subgraph_bar.append(node_a)
        assert format(graph, "graphviz") == uqbar.strings.normalize(
            """
            digraph G {
                subgraph cluster_foo {
                }
                subgraph bar {
                    b;
                    c;
                    a;
                    b -> c;
                    a -> b;
                    a -> c;
                }
            }
        """
        )
        subgraph_bar.remove(node_a)
        assert format(graph, "graphviz") == uqbar.strings.normalize(
            """
            digraph G {
                subgraph cluster_foo {
                }
                subgraph bar {
                    b;
                    c;
                    b -> c;
                }
            }
        """
        )

    def test_initialized_with_attributes(self):
        graph = uqbar.graphs.Graph(
            name="g",
            attributes=dict(
                bgcolor="transparent",
                color="lightslategrey",
                dpi=72,
                fontname="Arial",
                outputorder="edgesfirst",
                overlap="prism",
                rankdir="LR",
                ranksep=1,
                splines="spline",
                style=("dotted", "rounded"),
            ),
            edge_attributes=dict(penwidth=2),
            node_attributes=dict(
                fontname="Arial", fontsize=12, penwidth=2, style=("filled", "rounded")
            ),
        )
        assert format(graph, "graphviz") == uqbar.strings.normalize(
            """
            digraph g {
                graph [bgcolor=transparent,
                    color=lightslategrey,
                    dpi=72,
                    fontname=Arial,
                    outputorder=edgesfirst,
                    overlap=prism,
                    rankdir=LR,
                    ranksep=1,
                    splines=spline,
                    style="dotted, rounded"];
                node [fontname=Arial,
                    fontsize=12,
                    penwidth=2,
                    style="filled, rounded"];
                edge [penwidth=2];
            }
        """
        )
