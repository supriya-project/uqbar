import unittest

import uqbar.containers


class TestCase(unittest.TestCase):
    def test___init___01(self):
        """
        Initialize without name.
        """
        node = uqbar.containers.UniqueTreeNode()
        assert node.name is None
        assert node.parent is None
        assert node.depth == 0

    def test___init___02(self):
        """
        Initialize with name.
        """
        node = uqbar.containers.UniqueTreeNode(name="foo")
        assert node.name == "foo"
        assert node.parent is None
        assert node.depth == 0

    def test_name_01(self):
        node = uqbar.containers.UniqueTreeNode(name="foo")
        node.name = "bar"
        assert node.name == "bar"

    def test_name_02(self):
        node_a = uqbar.containers.UniqueTreeList()
        node_b = uqbar.containers.UniqueTreeList()
        node_c = uqbar.containers.UniqueTreeNode(name="foo")
        node_d = uqbar.containers.UniqueTreeList()
        node_a.append(node_b)
        node_b.append(node_c)
        assert node_a["foo"] is node_c
        assert node_b["foo"] is node_c
        with self.assertRaises(KeyError):
            node_d["foo"]
        node_c.name = "bar"
        assert node_a["bar"] is node_c
        assert node_b["bar"] is node_c
        with self.assertRaises(KeyError):
            node_a["foo"]
        with self.assertRaises(KeyError):
            node_b["foo"]
        with self.assertRaises(KeyError):
            node_d["bar"]
        node_d.append(node_c)
        assert node_d["bar"] is node_c
        with self.assertRaises(KeyError):
            node_a["bar"]
        with self.assertRaises(KeyError):
            node_b["bar"]
