import unittest

import uqbar.graphs
from uqbar.strings import normalize


class TestCase(unittest.TestCase):
    def test_mode(self):
        uqbar.graphs.Attributes(mode="cluster")
        uqbar.graphs.Attributes(mode="edge")
        uqbar.graphs.Attributes(mode="graph")
        uqbar.graphs.Attributes(mode="node")

    def test___format___str_01(self):
        attributes = uqbar.graphs.Attributes(mode="node")
        assert format(attributes) == repr(attributes)

    def test___format___str_02(self):
        attributes = uqbar.graphs.Attributes(
            mode="node",
            color="blue",
            fontname="Times New Roman",
            fontsize=11.5,
            shape="oval",
        )
        assert format(attributes) == repr(attributes)

    def test___format___graphviz_01(self):
        attributes = uqbar.graphs.Attributes(mode="node")
        assert format(attributes, "graphviz") == ""

    def test___format___graphviz_02(self):
        attributes = uqbar.graphs.Attributes(
            mode="node",
            color="blue",
            fontname="Times New Roman",
            fontsize=11.5,
            shape="oval",
        )
        assert format(attributes, "graphviz") == normalize(
            """
            [color=blue,
                fontname="Times New Roman",
                fontsize=11.5,
                shape=oval];
            """
        )
