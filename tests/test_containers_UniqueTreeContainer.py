import unittest

import uqbar.containers


class TestCase(unittest.TestCase):
    def test___init___01(self):
        """
        Initialize without name.
        """
        node = uqbar.containers.UniqueTreeList()
        assert node.name is None
        assert node.parent is None
        assert node.depth == 0
        assert len(node) == 0

    def test___init___02(self):
        """
        Initialize with name.
        """
        node = uqbar.containers.UniqueTreeList(name="foo")
        assert node.name == "foo"
        assert node.parent is None
        assert node.depth == 0
        assert len(node) == 0

    def test_append_01(self):
        """
        Unique parentage.
        """
        node_a = uqbar.containers.UniqueTreeList()
        node_b = uqbar.containers.UniqueTreeList()
        node_c = uqbar.containers.UniqueTreeNode()
        node_a.append(node_c)
        assert node_c.parent is node_a
        assert node_c in node_a
        assert len(node_a) == 1
        node_b.append(node_c)
        assert node_c.parent is node_b
        assert node_c in node_b
        assert len(node_b) == 1
        assert node_c not in node_a
        assert len(node_a) == 0

    def test_append_02(self):
        """
        Re-insertion.
        """
        node_a = uqbar.containers.UniqueTreeList()
        node_b = uqbar.containers.UniqueTreeNode()
        node_c = uqbar.containers.UniqueTreeNode()
        node_a.append(node_b)
        node_a.append(node_c)
        assert node_a is node_b.parent
        assert len(node_a) == 2
        assert node_a[:] == [node_b, node_c]
        assert node_b in node_a
        assert node_c in node_a
        node_a.append(node_b)
        assert node_a is node_b.parent
        assert len(node_a) == 2
        assert node_a[:] == [node_c, node_b]
        assert node_b in node_a
        assert node_c in node_a

    def test_extend_01(self):
        """
        Extend from a list.
        """
        node_a = uqbar.containers.UniqueTreeList()
        node_b = uqbar.containers.UniqueTreeNode()
        node_c = uqbar.containers.UniqueTreeNode()
        node_a.extend([node_b, node_c])
        assert len(node_a) == 2
        assert node_a is node_b.parent
        assert node_a is node_c.parent
        assert node_a[:] == [node_b, node_c]
        assert node_b in node_a
        assert node_c in node_a

    def test_extend_02(self):
        """
        Extend from another UniqueTreeList.
        """
        node_a = uqbar.containers.UniqueTreeList()
        node_b = uqbar.containers.UniqueTreeList()
        node_c = uqbar.containers.UniqueTreeNode()
        node_d = uqbar.containers.UniqueTreeNode()
        node_a.extend([node_c, node_d])
        assert len(node_a) == 2
        assert node_a is node_c.parent
        assert node_a is node_d.parent
        assert node_a[:] == [node_c, node_d]
        assert node_c in node_a
        assert node_d in node_a
        node_b.extend(node_a)
        assert len(node_a) == 0
        assert len(node_b) == 2
        assert node_a[:] == []
        assert node_b is node_c.parent
        assert node_b is node_d.parent
        assert node_b[:] == [node_c, node_d]
        assert node_c in node_b
        assert node_c not in node_a
        assert node_d in node_b
        assert node_d not in node_a

    def test_forbid_circular_parentage(self):
        """
        Cannot insert a parent as a child.
        """
        node_a = uqbar.containers.UniqueTreeList()
        node_b = uqbar.containers.UniqueTreeList()
        node_c = uqbar.containers.UniqueTreeList()
        node_a.append(node_b)
        node_b.append(node_c)
        with self.assertRaises(ValueError):
            node_c.append(node_a)

    def test___getitem___numbered(self):
        """
        UniqueTreeList can be subscripted with integers.
        """
        node_a = uqbar.containers.UniqueTreeList()
        node_b = uqbar.containers.UniqueTreeNode()
        node_c = uqbar.containers.UniqueTreeNode()
        node_d = uqbar.containers.UniqueTreeNode()
        node_a.extend([node_b, node_c, node_d])
        assert node_a[0] is node_b
        assert node_a[1] is node_c
        assert node_a[2] is node_d
        with self.assertRaises(IndexError):
            node_a[3]
        assert node_a[-1] is node_d
        assert node_a[-2] is node_c
        assert node_a[-3] is node_b
        with self.assertRaises(IndexError):
            node_a[-4]

    def test___getitem___named(self):
        """
        UniqueTreeList can be strings.

        Nodes are returned regardless how deep they are.
        """
        node_a = uqbar.containers.UniqueTreeList(name="foo")
        node_b = uqbar.containers.UniqueTreeList(name="bar")
        node_c = uqbar.containers.UniqueTreeNode(name="baz")
        node_d = uqbar.containers.UniqueTreeNode(name="quux")
        node_e = uqbar.containers.UniqueTreeNode(name="quux")
        node_a.extend([node_b, node_e])
        node_b.extend([node_c, node_d])
        with self.assertRaises(KeyError):
            node_a["foo"]
        assert node_a["bar"] is node_b
        assert node_a["baz"] is node_c
        assert node_a["quux"] == [node_d, node_e]

    def test___iter__(self):
        """
        UniqueTreeList can be iterated.
        """
        node_a = uqbar.containers.UniqueTreeList()
        node_b = uqbar.containers.UniqueTreeNode()
        node_c = uqbar.containers.UniqueTreeNode()
        node_d = uqbar.containers.UniqueTreeNode()
        node_a.extend([node_b, node_c, node_d])
        iterator = iter(node_a)
        assert next(iterator) is node_b
        assert next(iterator) is node_c
        assert next(iterator) is node_d
        with self.assertRaises(StopIteration):
            next(iterator)

    def test___len__(self):
        """
        Length-checking works.
        """
        node_a = uqbar.containers.UniqueTreeList()
        node_b = uqbar.containers.UniqueTreeNode()
        node_c = uqbar.containers.UniqueTreeNode()
        node_d = uqbar.containers.UniqueTreeNode()
        assert len(node_a) == 0
        node_a.append(node_b)
        assert len(node_a) == 1
        node_a.append(node_c)
        assert len(node_a) == 2
        node_a.append(node_d)
        assert len(node_a) == 3
        node_a.remove(node_b)
        assert len(node_a) == 2
        node_a.remove(node_c)
        assert len(node_a) == 1
        node_a.remove(node_d)
        assert len(node_a) == 0

    def test___setitem__(self):
        """
        Nodes can be set.
        """
        node_a = uqbar.containers.UniqueTreeList()
        node_b = uqbar.containers.UniqueTreeNode()
        node_c = uqbar.containers.UniqueTreeNode()
        node_d = uqbar.containers.UniqueTreeNode()
        node_a.extend([node_b, node_c])
        assert node_a[:] == [node_b, node_c]
        node_a[0] = node_d
        assert node_a[:] == [node_d, node_c]
        node_a[1:] = [node_b]
        assert node_a[:] == [node_d, node_b]
        node_a[:] = [node_c]
        assert node_a[:] == [node_c]
        node_a[:] = []
        assert node_a[:] == []

    def test___delitem___01(self):
        """
        Nodes can be deleted.
        """
        node_a = uqbar.containers.UniqueTreeList()
        node_b = uqbar.containers.UniqueTreeNode(name="foo")
        node_c = uqbar.containers.UniqueTreeNode(name="bar")
        node_d = uqbar.containers.UniqueTreeNode(name="baz")
        node_a.extend([node_b, node_c, node_d])
        del node_a[1]
        assert node_a[:] == [node_b, node_d]
        del node_a["baz"]
        assert node_a[:] == [node_b]

    def test___delitem___02(self):
        """
        Discontiguous named deletion works.
        """
        node_a = uqbar.containers.UniqueTreeList(name="foo")
        node_b = uqbar.containers.UniqueTreeList(name="bar")
        node_c = uqbar.containers.UniqueTreeNode(name="baz")
        node_d = uqbar.containers.UniqueTreeNode(name="quux")
        node_e = uqbar.containers.UniqueTreeNode(name="quux")
        node_a.extend([node_b, node_e])
        node_b.extend([node_c, node_d])
        del node_a["quux"]
        assert node_d.parent is None
        assert node_e.parent is None

    def test_pop(self):
        """
        Nodes can be popped.
        """
        node_a = uqbar.containers.UniqueTreeList()
        node_b = uqbar.containers.UniqueTreeNode()
        node_c = uqbar.containers.UniqueTreeNode()
        node_d = uqbar.containers.UniqueTreeNode()
        node_a.extend([node_b, node_c, node_d])
        assert node_a[:] == [node_b, node_c, node_d]
        assert node_a.pop() is node_d
        assert node_a[:] == [node_b, node_c]
        assert node_a.pop(0) is node_b
        assert node_a[:] == [node_c]
        assert node_a.pop(-1) is node_c
        assert node_a[:] == []
        assert node_b.parent is None
        assert node_c.parent is None
        assert node_d.parent is None

    def test_insert(self):
        """
        Nodes can be inserted.
        """
        node_a = uqbar.containers.UniqueTreeList()
        node_b = uqbar.containers.UniqueTreeNode()
        node_c = uqbar.containers.UniqueTreeNode()
        node_d = uqbar.containers.UniqueTreeNode()
        node_a.extend([node_b, node_c])
        assert node_a.insert(1, node_d) is None
        assert node_a is node_d.parent
        assert node_a[:] == [node_b, node_d, node_c]

    def test_remove(self):
        """
        Nodes can be removed.
        """
        node_a = uqbar.containers.UniqueTreeList()
        node_b = uqbar.containers.UniqueTreeNode()
        node_c = uqbar.containers.UniqueTreeNode()
        node_d = uqbar.containers.UniqueTreeNode()
        node_a.extend([node_b, node_c, node_d])
        assert node_a.remove(node_c) is None
        assert node_a[:] == [node_b, node_d]
        assert node_c not in node_a
        assert node_c.parent is None
