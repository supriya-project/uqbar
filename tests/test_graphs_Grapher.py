from unittest import mock

from uqbar import graphs


def test_01(tmp_path):
    graph = graphs.Graph()
    node_a = graphs.Node()
    node_b = graphs.Node()
    node_a.attach(node_b)
    graph.extend([node_a, node_b])
    assert list(tmp_path.iterdir()) == []
    with mock.patch.object(graphs.Grapher, "open_output_path") as patcher:
        graphs.Grapher(graph, output_directory=tmp_path)()
    assert patcher.call_count == 1
    for glob in ["*.dot", "*.log", "*.pdf"]:
        assert len(list(tmp_path.glob(glob))) == 1
