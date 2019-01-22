import unittest

import uqbar.graphs
from uqbar.strings import normalize


class TestCase(unittest.TestCase):
    def test___init__(self):
        node_a = uqbar.graphs.Node(name="foo")
        node_b = uqbar.graphs.Node(name="bar")
        uqbar.graphs.Edge().attach(node_a, node_b)

    def test___format___str(self):
        node_a = uqbar.graphs.Node(name="foo")
        node_b = uqbar.graphs.Node(name="bar")
        edge = uqbar.graphs.Edge().attach(node_a, node_b)
        assert format(edge) == repr(edge)

        node_a = uqbar.graphs.Node(name="foo")
        node_b = uqbar.graphs.Node(name="bar")
        attributes = uqbar.graphs.Attributes(
            mode="edge", color="blue", style=["dotted"]
        )
        edge = uqbar.graphs.Edge(attributes=attributes).attach(node_a, node_b)
        assert format(edge) == repr(edge)

    def test___format___graphviz(self):
        node_a = uqbar.graphs.Node(name="foo")
        node_b = uqbar.graphs.Node(name="bar")
        edge = uqbar.graphs.Edge().attach(node_a, node_b)
        assert format(edge, "graphviz") == "foo -> bar;"

        node_a = uqbar.graphs.Node(name="foo")
        node_b = uqbar.graphs.Node(name="bar")
        attributes = uqbar.graphs.Attributes(
            mode="edge", color="blue", style=["dotted"]
        )
        edge = uqbar.graphs.Edge(attributes=attributes).attach(node_a, node_b)
        assert format(edge, "graphviz") == normalize(
            """
            foo -> bar [color=blue,
                style=dotted];
        """
        )
