import unittest
import uqbar.containers


class TestCase(unittest.TestCase):

    def test___init___01(self):
        node = uqbar.containers.UniqueTreeNode()
        assert node.name is None
        assert node.parent is None
        assert node.depth == 0

    def test___init___02(self):
        node = uqbar.containers.UniqueTreeNode(name='foo')
        assert node.name == 'foo'
        assert node.parent is None
        assert node.depth == 0
