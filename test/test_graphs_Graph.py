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

    def test_functional(self):
        # instantiate them
        graph = uqbar.graphs.Graph(name='G')
        cluster_0 = uqbar.graphs.Graph(name='0', is_cluster=True)
        cluster_1 = uqbar.graphs.Graph(name='1', is_cluster=True)
        a0 = uqbar.graphs.Node(name='a0')
        a1 = uqbar.graphs.Node(name='a1')
        a2 = uqbar.graphs.Node(name='a2')
        a3 = uqbar.graphs.Node(name='a3')
        b0 = uqbar.graphs.Node(name='b0')
        b1 = uqbar.graphs.Node(name='b1')
        b2 = uqbar.graphs.Node(name='b2')
        b3 = uqbar.graphs.Node(name='b3')
        start = uqbar.graphs.Node(name='start')
        end = uqbar.graphs.Node(name='end')
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
        cluster_0.attributes['style'] = 'filled'
        cluster_0.attributes['color'] = 'lightgrey'
        cluster_0.attributes['label'] = 'process #1'
        cluster_0.node_attributes['style'] = 'filled'
        cluster_0.node_attributes['color'] = 'white'
        cluster_1.attributes['color'] = 'blue'
        cluster_1.attributes['label'] = 'process #2'
        cluster_1.node_attributes['style'] = ('filled', 'rounded')
        start.attributes['shape'] = 'Mdiamond'
        end.attributes['shape'] = 'Msquare'
        # format them
        assert format(graph) == repr(graph)
        assert format(graph, 'graphviz') == self.normalize('''
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
        ''')
