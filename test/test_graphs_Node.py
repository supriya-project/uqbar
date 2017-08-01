import textwrap
import unittest
import uqbar.graphs


class TestCase(unittest.TestCase):

    def normalize(self, string):
        lines = [
            line.rstrip() for line in
            string.replace('\t', '    ').split('\n')
            ]
        while not lines[0]:
            lines.pop(0)
        while not lines[-1]:
            lines.pop()
        string = '\n'.join(lines)
        return textwrap.dedent(string)

    def test___init__(self):
        node = uqbar.graphs.Node()
        assert node.name is None

        node = uqbar.graphs.Node(name='foo')
        assert node.name == 'foo'
        assert not node.attributes

        attributes = uqbar.graphs.Attributes(mode='node', color='blue')
        node = uqbar.graphs.Node(name='foo', attributes=attributes)
        assert node.name == 'foo'
        assert len(node.attributes) == 1
        assert node.attributes['color'] == node.attributes.Color('blue')
