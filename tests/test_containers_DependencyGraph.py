import pytest

import uqbar.containers


def test___contains__():
    graph = uqbar.containers.DependencyGraph()
    assert "A" not in graph
    assert "B" not in graph
    graph.add("A")
    assert "A" in graph
    assert "B" not in graph
    graph.add("B", parent="A")
    assert "A" in graph
    assert "B" in graph
    graph.remove("A")
    assert "A" not in graph
    assert "B" in graph
    graph.remove("B")
    assert "A" not in graph
    assert "B" not in graph


def test___eq__():
    graph_one = uqbar.containers.DependencyGraph()
    graph_two = uqbar.containers.DependencyGraph()
    graph_three = uqbar.containers.DependencyGraph()
    assert graph_one == graph_two
    assert graph_one != "foo"
    graph_one.add("A", parent="B")
    graph_one.add("C", parent="B")
    assert graph_one != graph_two
    graph_two.add("C", parent="B")
    graph_two.add("A", parent="B")
    assert graph_one != graph_two
    graph_three.add("C", parent="B")
    graph_three.add("A", parent="B")
    assert graph_two == graph_three


def test___getitem__():
    graph = uqbar.containers.DependencyGraph()
    graph.add("B", parent="A")
    graph.add("C", parent="A")
    graph.add("D", parent="A")
    graph.add("D", parent="B")
    assert graph["A"] == (frozenset([]), frozenset(["B", "C", "D"]))
    assert graph["B"] == (frozenset(["A"]), frozenset(["D"]))
    assert graph["C"] == (frozenset(["A"]), frozenset([]))
    assert graph["D"] == (frozenset(["A", "B"]), frozenset([]))


def test___iter__():
    graph = uqbar.containers.DependencyGraph()
    graph.add("A")
    graph.add("B", parent="A")
    graph.add("C", parent="A")
    graph.add("D", parent="B")
    graph.add("D", parent="C")
    graph.add("E", parent="A")
    assert list(graph) == ["D", "B", "C", "E", "A"]
    assert list(graph) == ["D", "B", "C", "E", "A"]  # non-destructive
    graph.remove("A")
    assert list(graph) == ["D", "B", "C", "E"]
    graph.remove("C")
    assert list(graph) == ["D", "B", "E"]


def test___len__():
    graph = uqbar.containers.DependencyGraph()
    assert len(graph) == 0
    graph.add("A")
    assert len(graph) == 1
    graph.add("B", parent="A")
    assert len(graph) == 2
    graph.add("C", parent="A")
    assert len(graph) == 3
    graph.remove("A")
    assert len(graph) == 2
    graph.remove("B")
    assert len(graph) == 1
    graph.remove("C")
    assert len(graph) == 0


def test_add():
    graph = uqbar.containers.DependencyGraph()
    graph.add("A")
    assert "A" in graph
    graph.add("B", parent="C")
    assert "B" in graph
    assert "C" in graph
    graph.add("B", parent="A")
    assert "A" in graph
    assert "B" in graph
    assert "C" in graph


def test_children():
    graph = uqbar.containers.DependencyGraph()
    graph.add("B", parent="A")
    graph.add("C", parent="A")
    graph.add("D")
    graph.add("E", parent="A")
    graph.add("E", parent="D")
    assert graph.children("A") == frozenset(["B", "C", "E"])
    assert graph.children("B") == frozenset([])
    assert graph.children("C") == frozenset([])
    assert graph.children("D") == frozenset(["E"])
    assert graph.children("E") == frozenset([])


def test_copy():
    graph_one = uqbar.containers.DependencyGraph()
    graph_one.add("A", parent="B")
    graph_one.add("C", parent="B")
    graph_two = graph_one.copy()
    assert graph_one == graph_two
    assert graph_one is not graph_two
    graph_one.remove("B")
    assert graph_one != graph_two


def test_is_acyclic():
    graph = uqbar.containers.DependencyGraph()
    assert graph.is_acyclic()
    graph.add("A")
    assert graph.is_acyclic()
    graph.add("B", parent="A")
    assert graph.is_acyclic()
    graph.add("C", parent="B")
    assert graph.is_acyclic()
    graph.add("A", parent="C")
    assert not graph.is_acyclic()
    graph.remove("B")
    assert graph.is_acyclic()


def test_parents():
    graph = uqbar.containers.DependencyGraph()
    graph.add("B", parent="A")
    graph.add("C", parent="A")
    graph.add("D")
    graph.add("E", parent="A")
    graph.add("E", parent="D")
    assert graph.parents("A") == frozenset([])
    assert graph.parents("B") == frozenset(["A"])
    assert graph.parents("C") == frozenset(["A"])
    assert graph.parents("D") == frozenset([])
    assert graph.parents("E") == frozenset(["A", "D"])


def test_remove():
    graph = uqbar.containers.DependencyGraph()
    with pytest.raises(ValueError):
        graph.remove("A")
    assert "A" not in graph
    graph.add("A")
    assert "A" in graph
    graph.remove("A")
    assert "A" not in graph
