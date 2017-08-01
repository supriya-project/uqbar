import textwrap
import unittest
import uqbar.graphs


class TestCase(unittest.TestCase):

    def normalize(self, string):
        lines = [
            line.rstrip() for line in
            string.replace('\t', '    ').split('\n')
            ]
        if not lines:
            return ''
        while lines and not lines[0]:
            lines.pop(0)
        while lines and not lines[-1]:
            lines.pop()
        string = '\n'.join(lines)
        return textwrap.dedent(string)

    def test___init__(self):
        node_a = uqbar.graphs.Node(name='foo')
        node_b = uqbar.graphs.Node(name='bar')
        uqbar.graphs.Edge(node_a, node_b)

    def test___format___str(self):
        node_a = uqbar.graphs.Node(name='foo')
        node_b = uqbar.graphs.Node(name='bar')
        edge = uqbar.graphs.Edge(node_a, node_b)
        assert format(edge) == repr(edge)

        node_a = uqbar.graphs.Node(name='foo')
        node_b = uqbar.graphs.Node(name='bar')
        attributes = uqbar.graphs.Attributes(
            mode='edge',
            color='blue',
            style=['dotted'],
            )
        edge = uqbar.graphs.Edge(node_a, node_b, attributes=attributes)
        assert format(edge) == repr(edge)

    def test___format___graphviz(self):
        node_a = uqbar.graphs.Node(name='foo')
        node_b = uqbar.graphs.Node(name='bar')
        edge = uqbar.graphs.Edge(node_a, node_b)
        assert format(edge, 'graphviz') == 'foo -> bar;'

        node_a = uqbar.graphs.Node(name='foo')
        node_b = uqbar.graphs.Node(name='bar')
        attributes = uqbar.graphs.Attributes(
            mode='edge',
            color='blue',
            style=['dotted'],
            )
        edge = uqbar.graphs.Edge(node_a, node_b, attributes=attributes)
        assert format(edge, 'graphviz') == self.normalize('''
            foo -> bar [color=blue,
                style=dotted];
        ''')
