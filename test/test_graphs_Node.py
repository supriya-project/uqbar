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

    def test__get_canonical_name(self):
        node = uqbar.graphs.Node()
        assert node._get_canonical_name() == 'node_0'

        node = uqbar.graphs.Node(name='foo')
        assert node._get_canonical_name() == 'node_foo'

        node = uqbar.graphs.Node(name='Foo Bar Baz')
        assert node._get_canonical_name() == 'node_Foo Bar Baz'

        graph = uqbar.graphs.Graph()
        node = uqbar.graphs.Node()
        graph.append(node)
        assert node._get_canonical_name() == 'node_0'

        graph = uqbar.graphs.Graph()
        subgraph = uqbar.graphs.Graph()
        node = uqbar.graphs.Node()
        graph.append(subgraph)
        subgraph.append(node)
        assert node._get_canonical_name() == 'node_0_0'

        graph = uqbar.graphs.Graph()
        node_a = uqbar.graphs.Node(name='foo')
        node_b = uqbar.graphs.Node(name='foo')
        node_c = uqbar.graphs.Node(name='bar')
        graph.extend([node_a, node_b, node_c])
        assert node_a._get_canonical_name() == 'node_foo_0'
        assert node_b._get_canonical_name() == 'node_foo_1'
        assert node_c._get_canonical_name() == 'node_bar'

    def test___format___str(self):
        node = uqbar.graphs.Node()
        assert format(node) == repr(node)

        node = uqbar.graphs.Node(name='foo')
        assert format(node) == repr(node)

        attributes = uqbar.graphs.Attributes(mode='node', color='blue')
        node = uqbar.graphs.Node(name='foo', attributes=attributes)
        assert format(node) == repr(node)

    def test___format___graphviz(self):
        node = uqbar.graphs.Node()
        assert format(node, 'graphviz') == 'node_0;'

        node = uqbar.graphs.Node(name='foo')
        assert format(node, 'graphviz') == 'node_foo;'

        attributes = uqbar.graphs.Attributes(
            mode='node',
            color='blue',
            fontname='Times New Roman',
            fontsize=11.5,
            shape='oval',
            )
        node = uqbar.graphs.Node(name='foo', attributes=attributes)
        assert format(node, 'graphviz') == self.normalize('''
            node_foo [color=blue,
                fontname="Times New Roman",
                fontsize=11.5,
                shape=oval];
        ''')
