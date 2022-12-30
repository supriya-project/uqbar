import collections
import pickle
import sys

import pytest

import uqbar.apis
import uqbar.apis.dummy
import uqbar.strings


def test_01():
    inheritance_graph = uqbar.apis.InheritanceGraph(package_paths=["uqbar.containers"])
    assert str(inheritance_graph) == uqbar.strings.normalize(
        r"""
            digraph InheritanceGraph {
                graph [bgcolor=transparent,
                    color=lightsteelblue2,
                    fontname=Arial,
                    fontsize=10,
                    outputorder=edgesfirst,
                    overlap=prism,
                    penwidth=2,
                    rankdir=LR,
                    splines=spline,
                    style="dashed, rounded",
                    truecolor=true];
                node [colorscheme=pastel19,
                    fontname=Arial,
                    fontsize=10,
                    height=0,
                    penwidth=2,
                    shape=box,
                    style="filled, rounded",
                    width=0];
                edge [color=lightslategrey,
                    penwidth=1];
                subgraph cluster_builtins {
                    graph [label=builtins];
                    node [color=1];
                    "builtins.object" [label=object];
                }
                subgraph "cluster_uqbar.containers.dependency_graph" {
                    graph [label="uqbar.containers.dependency_graph"];
                    node [color=2];
                    "uqbar.containers.dependency_graph.DependencyGraph" [label="Dependency\nGraph"];
                }
                subgraph "cluster_uqbar.containers.unique_tree" {
                    graph [label="uqbar.containers.unique_tree"];
                    node [color=3];
                    "uqbar.containers.unique_tree.UniqueTreeContainer" [label="Unique\nTree\nContainer"];
                    "uqbar.containers.unique_tree.UniqueTreeDict" [label="Unique\nTree\nDict"];
                    "uqbar.containers.unique_tree.UniqueTreeList" [label="Unique\nTree\nList"];
                    "uqbar.containers.unique_tree.UniqueTreeNode" [label="Unique\nTree\nNode"];
                    "uqbar.containers.unique_tree.UniqueTreeSet" [label="Unique\nTree\nSet"];
                    "uqbar.containers.unique_tree.UniqueTreeTuple" [label="Unique\nTree\nTuple"];
                    "uqbar.containers.unique_tree.UniqueTreeContainer" -> "uqbar.containers.unique_tree.UniqueTreeDict";
                    "uqbar.containers.unique_tree.UniqueTreeContainer" -> "uqbar.containers.unique_tree.UniqueTreeList";
                    "uqbar.containers.unique_tree.UniqueTreeContainer" -> "uqbar.containers.unique_tree.UniqueTreeSet";
                    "uqbar.containers.unique_tree.UniqueTreeContainer" -> "uqbar.containers.unique_tree.UniqueTreeTuple";
                    "uqbar.containers.unique_tree.UniqueTreeNode" -> "uqbar.containers.unique_tree.UniqueTreeContainer";
                }
                "builtins.object" -> "uqbar.containers.dependency_graph.DependencyGraph";
                "builtins.object" -> "uqbar.containers.unique_tree.UniqueTreeNode";
            }
        """
    )
    pickle.dumps(inheritance_graph)


def test_02():
    inheritance_graph = uqbar.apis.InheritanceGraph(
        package_paths=["uqbar"], lineage_paths=["uqbar.containers"]
    )
    assert str(inheritance_graph) == uqbar.strings.normalize(
        r"""
            digraph InheritanceGraph {
                graph [bgcolor=transparent,
                    color=lightsteelblue2,
                    fontname=Arial,
                    fontsize=10,
                    outputorder=edgesfirst,
                    overlap=prism,
                    penwidth=2,
                    rankdir=LR,
                    splines=spline,
                    style="dashed, rounded",
                    truecolor=true];
                node [colorscheme=pastel19,
                    fontname=Arial,
                    fontsize=10,
                    height=0,
                    penwidth=2,
                    shape=box,
                    style="filled, rounded",
                    width=0];
                edge [color=lightslategrey,
                    penwidth=1];
                subgraph cluster_builtins {
                    graph [label=builtins];
                    node [color=1];
                    "builtins.object" [label=object];
                }
                subgraph "cluster_uqbar.apis.nodes" {
                    graph [label="uqbar.apis.nodes"];
                    node [color=2];
                    "uqbar.apis.nodes.ModuleNode" [label="Module\nNode"];
                    "uqbar.apis.nodes.PackageNode" [label="Package\nNode"];
                }
                subgraph "cluster_uqbar.containers.dependency_graph" {
                    graph [label="uqbar.containers.dependency_graph"];
                    node [color=3];
                    "uqbar.containers.dependency_graph.DependencyGraph" [label="Dependency\nGraph"];
                }
                subgraph "cluster_uqbar.containers.unique_tree" {
                    graph [label="uqbar.containers.unique_tree"];
                    node [color=4];
                    "uqbar.containers.unique_tree.UniqueTreeContainer" [label="Unique\nTree\nContainer"];
                    "uqbar.containers.unique_tree.UniqueTreeDict" [label="Unique\nTree\nDict"];
                    "uqbar.containers.unique_tree.UniqueTreeList" [label="Unique\nTree\nList"];
                    "uqbar.containers.unique_tree.UniqueTreeNode" [label="Unique\nTree\nNode"];
                    "uqbar.containers.unique_tree.UniqueTreeSet" [label="Unique\nTree\nSet"];
                    "uqbar.containers.unique_tree.UniqueTreeTuple" [label="Unique\nTree\nTuple"];
                    "uqbar.containers.unique_tree.UniqueTreeContainer" -> "uqbar.containers.unique_tree.UniqueTreeDict";
                    "uqbar.containers.unique_tree.UniqueTreeContainer" -> "uqbar.containers.unique_tree.UniqueTreeList";
                    "uqbar.containers.unique_tree.UniqueTreeContainer" -> "uqbar.containers.unique_tree.UniqueTreeSet";
                    "uqbar.containers.unique_tree.UniqueTreeContainer" -> "uqbar.containers.unique_tree.UniqueTreeTuple";
                    "uqbar.containers.unique_tree.UniqueTreeNode" -> "uqbar.containers.unique_tree.UniqueTreeContainer";
                }
                subgraph "cluster_uqbar.graphs.core" {
                    graph [label="uqbar.graphs.core"];
                    node [color=5];
                    "uqbar.graphs.core.Attachable" [label=Attachable];
                    "uqbar.graphs.core.Graph" [label="Graph"];
                    "uqbar.graphs.core.Node" [label="Node"];
                }
                subgraph "cluster_uqbar.graphs.html" {
                    graph [label="uqbar.graphs.html"];
                    node [color=6];
                    "uqbar.graphs.html.HRule" [label=HRule];
                    "uqbar.graphs.html.LineBreak" [label="Line\nBreak"];
                    "uqbar.graphs.html.Table" [label=Table];
                    "uqbar.graphs.html.TableCell" [label="Table\nCell"];
                    "uqbar.graphs.html.TableRow" [label="Table\nRow"];
                    "uqbar.graphs.html.Text" [label=Text];
                    "uqbar.graphs.html.VRule" [label=VRule];
                }
                subgraph "cluster_uqbar.graphs.records" {
                    graph [label="uqbar.graphs.records"];
                    node [color=7];
                    "uqbar.graphs.records.RecordField" [label="Record\nField"];
                    "uqbar.graphs.records.RecordGroup" [label="Record\nGroup"];
                }
                "builtins.object" -> "uqbar.containers.dependency_graph.DependencyGraph";
                "builtins.object" -> "uqbar.containers.unique_tree.UniqueTreeNode";
                "uqbar.containers.unique_tree.UniqueTreeList" -> "uqbar.apis.nodes.PackageNode";
                "uqbar.containers.unique_tree.UniqueTreeList" -> "uqbar.graphs.core.Graph";
                "uqbar.containers.unique_tree.UniqueTreeList" -> "uqbar.graphs.core.Node";
                "uqbar.containers.unique_tree.UniqueTreeList" -> "uqbar.graphs.html.Table";
                "uqbar.containers.unique_tree.UniqueTreeList" -> "uqbar.graphs.html.TableCell";
                "uqbar.containers.unique_tree.UniqueTreeList" -> "uqbar.graphs.html.TableRow";
                "uqbar.containers.unique_tree.UniqueTreeList" -> "uqbar.graphs.records.RecordGroup";
                "uqbar.containers.unique_tree.UniqueTreeNode" -> "uqbar.apis.nodes.ModuleNode";
                "uqbar.containers.unique_tree.UniqueTreeNode" -> "uqbar.graphs.core.Attachable";
                "uqbar.containers.unique_tree.UniqueTreeNode" -> "uqbar.graphs.html.HRule";
                "uqbar.containers.unique_tree.UniqueTreeNode" -> "uqbar.graphs.html.LineBreak";
                "uqbar.containers.unique_tree.UniqueTreeNode" -> "uqbar.graphs.html.Text";
                "uqbar.containers.unique_tree.UniqueTreeNode" -> "uqbar.graphs.html.VRule";
                "uqbar.containers.unique_tree.UniqueTreeNode" -> "uqbar.graphs.records.RecordField";
                "uqbar.graphs.core.Attachable" -> "uqbar.graphs.html.TableCell";
                "uqbar.graphs.core.Attachable" -> "uqbar.graphs.records.RecordField";
            }
        """
    )
    pickle.dumps(inheritance_graph)


@pytest.mark.xfail(
    sys.version_info.minor >= 11, reason="ReprEnum introduced in 3.11", strict=True
)
def test_03_py310():
    inheritance_graph = uqbar.apis.InheritanceGraph(
        package_paths=["uqbar"], lineage_paths=["uqbar"]
    )
    assert str(inheritance_graph) == uqbar.strings.normalize(
        r"""
            digraph InheritanceGraph {
                graph [bgcolor=transparent,
                    color=lightsteelblue2,
                    fontname=Arial,
                    fontsize=10,
                    outputorder=edgesfirst,
                    overlap=prism,
                    penwidth=2,
                    rankdir=LR,
                    splines=spline,
                    style="dashed, rounded",
                    truecolor=true];
                node [colorscheme=pastel19,
                    fontname=Arial,
                    fontsize=10,
                    height=0,
                    penwidth=2,
                    shape=box,
                    style="filled, rounded",
                    width=0];
                edge [color=lightslategrey,
                    penwidth=1];
                subgraph cluster_builtins {
                    graph [label=builtins];
                    node [color=1];
                    "builtins.BaseException" [label="Base\nException"];
                    "builtins.Exception" [label=Exception];
                    "builtins.int" [label=int];
                    "builtins.object" [label=object];
                    "builtins.BaseException" -> "builtins.Exception";
                    "builtins.object" -> "builtins.BaseException";
                    "builtins.object" -> "builtins.int";
                }
                subgraph cluster_code {
                    graph [label=code];
                    node [color=2];
                    "code.InteractiveConsole" [label="Interactive\nConsole"];
                    "code.InteractiveInterpreter" [label="Interactive\nInterpreter"];
                    "code.InteractiveInterpreter" -> "code.InteractiveConsole";
                }
                subgraph "cluster_collections.abc" {
                    graph [label="collections.abc"];
                    node [color=3];
                    "collections.abc.Collection" [label=Collection,
                        shape=oval,
                        style=bold];
                    "collections.abc.Container" [label=Container,
                        shape=oval,
                        style=bold];
                    "collections.abc.Iterable" [label=Iterable,
                        shape=oval,
                        style=bold];
                    "collections.abc.Mapping" [label=Mapping,
                        shape=oval,
                        style=bold];
                    "collections.abc.MutableMapping" [label="Mutable\nMapping",
                        shape=oval,
                        style=bold];
                    "collections.abc.Sized" [label=Sized,
                        shape=oval,
                        style=bold];
                    "collections.abc.Collection" -> "collections.abc.Mapping";
                    "collections.abc.Container" -> "collections.abc.Collection";
                    "collections.abc.Iterable" -> "collections.abc.Collection";
                    "collections.abc.Mapping" -> "collections.abc.MutableMapping";
                    "collections.abc.Sized" -> "collections.abc.Collection";
                }
                subgraph "cluster_docutils.nodes" {
                    graph [label="docutils.nodes"];
                    node [color=4];
                    "docutils.nodes.Body" [label=Body];
                    "docutils.nodes.Element" [label=Element];
                    "docutils.nodes.General" [label=General];
                    "docutils.nodes.Node" [label="Node"];
                    "docutils.nodes.Body" -> "docutils.nodes.General";
                    "docutils.nodes.Node" -> "docutils.nodes.Element";
                }
                subgraph "cluster_docutils.parsers.rst" {
                    graph [label="docutils.parsers.rst"];
                    node [color=5];
                    "docutils.parsers.rst.Directive" [label=Directive];
                }
                subgraph cluster_enum {
                    graph [label=enum];
                    node [color=6];
                    "enum.Enum" [label=Enum];
                    "enum.IntEnum" [label="Int\nEnum"];
                    "enum.Enum" -> "enum.IntEnum";
                }
                subgraph "cluster_uqbar.apis.builders" {
                    graph [label="uqbar.apis.builders"];
                    node [color=7];
                    "uqbar.apis.builders.APIBuilder" [label=APIBuilder];
                }
                subgraph "cluster_uqbar.apis.documenters" {
                    graph [label="uqbar.apis.documenters"];
                    node [color=8];
                    "uqbar.apis.documenters.ClassDocumenter" [label="Class\nDocumenter"];
                    "uqbar.apis.documenters.FunctionDocumenter" [label="Function\nDocumenter"];
                    "uqbar.apis.documenters.MemberDocumenter" [label="Member\nDocumenter"];
                    "uqbar.apis.documenters.ModuleDocumenter" [label="Module\nDocumenter"];
                    "uqbar.apis.documenters.RootDocumenter" [label="Root\nDocumenter"];
                    "uqbar.apis.documenters.MemberDocumenter" -> "uqbar.apis.documenters.ClassDocumenter";
                    "uqbar.apis.documenters.MemberDocumenter" -> "uqbar.apis.documenters.FunctionDocumenter";
                }
                subgraph "cluster_uqbar.apis.dummy" {
                    graph [label="uqbar.apis.dummy"];
                    node [color=9];
                    "uqbar.apis.dummy.MyChildClass" [label="My\nChild\nClass"];
                    "uqbar.apis.dummy.MyParentClass" [label="My\nParent\nClass"];
                    "uqbar.apis.dummy.MyParentClass" -> "uqbar.apis.dummy.MyChildClass";
                }
                subgraph "cluster_uqbar.apis.graphs" {
                    graph [label="uqbar.apis.graphs"];
                    node [color=1];
                    "uqbar.apis.graphs.InheritanceGraph" [label="Inheritance\nGraph"];
                }
                subgraph "cluster_uqbar.apis.nodes" {
                    graph [label="uqbar.apis.nodes"];
                    node [color=2];
                    "uqbar.apis.nodes.ModuleNode" [label="Module\nNode"];
                    "uqbar.apis.nodes.PackageNode" [label="Package\nNode"];
                }
                subgraph "cluster_uqbar.apis.summarizers" {
                    graph [label="uqbar.apis.summarizers"];
                    node [color=3];
                    "uqbar.apis.summarizers.ImmaterialClassDocumenter" [label="Immaterial\nClass\nDocumenter"];
                    "uqbar.apis.summarizers.ImmaterialModuleDocumenter" [label="Immaterial\nModule\nDocumenter"];
                    "uqbar.apis.summarizers.SummarizingClassDocumenter" [label="Summarizing\nClass\nDocumenter"];
                    "uqbar.apis.summarizers.SummarizingModuleDocumenter" [label="Summarizing\nModule\nDocumenter"];
                    "uqbar.apis.summarizers.SummarizingRootDocumenter" [label="Summarizing\nRoot\nDocumenter"];
                    "uqbar.apis.summarizers.SummarizingClassDocumenter" -> "uqbar.apis.summarizers.ImmaterialClassDocumenter";
                }
                subgraph "cluster_uqbar.book.console" {
                    graph [label="uqbar.book.console"];
                    node [color=4];
                    "uqbar.book.console.Console" [label=Console];
                    "uqbar.book.console.ConsoleError" [label="Console\nError"];
                    "uqbar.book.console.ConsoleInput" [label="Console\nInput"];
                    "uqbar.book.console.ConsoleOutput" [label="Console\nOutput"];
                    "uqbar.book.console.MonkeyPatch" [label="Monkey\nPatch"];
                }
                subgraph "cluster_uqbar.book.extensions" {
                    graph [label="uqbar.book.extensions"];
                    node [color=5];
                    "uqbar.book.extensions.Extension" [label=Extension];
                    "uqbar.book.extensions.GraphExtension" [label="Graph\nExtension"];
                    "uqbar.book.extensions.Extension" -> "uqbar.book.extensions.GraphExtension";
                }
                subgraph "cluster_uqbar.book.sphinx" {
                    graph [label="uqbar.book.sphinx"];
                    node [color=6];
                    "uqbar.book.sphinx.UqbarBookDefaultsDirective" [label="Uqbar\nBook\nDefaults\nDirective"];
                    "uqbar.book.sphinx.UqbarBookDirective" [label="Uqbar\nBook\nDirective"];
                    "uqbar.book.sphinx.UqbarBookImportDirective" [label="Uqbar\nBook\nImport\nDirective"];
                    "uqbar.book.sphinx.uqbar_book_defaults_block" [label="uqbar\nbook\ndefaults\nblock"];
                    "uqbar.book.sphinx.uqbar_book_import_block" [label="uqbar\nbook\nimport\nblock"];
                }
                subgraph "cluster_uqbar.containers.dependency_graph" {
                    graph [label="uqbar.containers.dependency_graph"];
                    node [color=7];
                    "uqbar.containers.dependency_graph.DependencyGraph" [label="Dependency\nGraph"];
                }
                subgraph "cluster_uqbar.containers.unique_tree" {
                    graph [label="uqbar.containers.unique_tree"];
                    node [color=8];
                    "uqbar.containers.unique_tree.UniqueTreeContainer" [label="Unique\nTree\nContainer"];
                    "uqbar.containers.unique_tree.UniqueTreeDict" [label="Unique\nTree\nDict"];
                    "uqbar.containers.unique_tree.UniqueTreeList" [label="Unique\nTree\nList"];
                    "uqbar.containers.unique_tree.UniqueTreeNode" [label="Unique\nTree\nNode"];
                    "uqbar.containers.unique_tree.UniqueTreeSet" [label="Unique\nTree\nSet"];
                    "uqbar.containers.unique_tree.UniqueTreeTuple" [label="Unique\nTree\nTuple"];
                    "uqbar.containers.unique_tree.UniqueTreeContainer" -> "uqbar.containers.unique_tree.UniqueTreeDict";
                    "uqbar.containers.unique_tree.UniqueTreeContainer" -> "uqbar.containers.unique_tree.UniqueTreeList";
                    "uqbar.containers.unique_tree.UniqueTreeContainer" -> "uqbar.containers.unique_tree.UniqueTreeSet";
                    "uqbar.containers.unique_tree.UniqueTreeContainer" -> "uqbar.containers.unique_tree.UniqueTreeTuple";
                    "uqbar.containers.unique_tree.UniqueTreeNode" -> "uqbar.containers.unique_tree.UniqueTreeContainer";
                }
                subgraph "cluster_uqbar.enums" {
                    graph [label="uqbar.enums"];
                    node [color=9];
                    "uqbar.enums.IntEnumeration" [label="Int\nEnumeration"];
                    "uqbar.enums.StrictEnumeration" [label="Strict\nEnumeration"];
                }
                subgraph "cluster_uqbar.graphs.attrs" {
                    graph [label="uqbar.graphs.attrs"];
                    node [color=1];
                    "uqbar.graphs.attrs.Attributes" [label=Attributes];
                }
                subgraph "cluster_uqbar.graphs.core" {
                    graph [label="uqbar.graphs.core"];
                    node [color=2];
                    "uqbar.graphs.core.Attachable" [label=Attachable];
                    "uqbar.graphs.core.Edge" [label="Edge"];
                    "uqbar.graphs.core.Graph" [label="Graph"];
                    "uqbar.graphs.core.Node" [label="Node"];
                }
                subgraph "cluster_uqbar.graphs.graphers" {
                    graph [label="uqbar.graphs.graphers"];
                    node [color=3];
                    "uqbar.graphs.graphers.Grapher" [label=Grapher];
                }
                subgraph "cluster_uqbar.graphs.html" {
                    graph [label="uqbar.graphs.html"];
                    node [color=4];
                    "uqbar.graphs.html.HRule" [label=HRule];
                    "uqbar.graphs.html.LineBreak" [label="Line\nBreak"];
                    "uqbar.graphs.html.Table" [label=Table];
                    "uqbar.graphs.html.TableCell" [label="Table\nCell"];
                    "uqbar.graphs.html.TableRow" [label="Table\nRow"];
                    "uqbar.graphs.html.Text" [label=Text];
                    "uqbar.graphs.html.VRule" [label=VRule];
                }
                subgraph "cluster_uqbar.graphs.records" {
                    graph [label="uqbar.graphs.records"];
                    node [color=5];
                    "uqbar.graphs.records.RecordField" [label="Record\nField"];
                    "uqbar.graphs.records.RecordGroup" [label="Record\nGroup"];
                }
                subgraph "cluster_uqbar.io" {
                    graph [label="uqbar.io"];
                    node [color=6];
                    "uqbar.io.DirectoryChange" [color=black,
                        fontcolor=white,
                        label="Directory\nChange"];
                    "uqbar.io.Profiler" [color=black,
                        fontcolor=white,
                        label=Profiler];
                    "uqbar.io.RedirectedStreams" [color=black,
                        fontcolor=white,
                        label="Redirected\nStreams"];
                    "uqbar.io.Timer" [color=black,
                        fontcolor=white,
                        label=Timer];
                }
                subgraph "cluster_uqbar.sphinx.inheritance" {
                    graph [label="uqbar.sphinx.inheritance"];
                    node [color=7];
                    "uqbar.sphinx.inheritance.InheritanceDiagram" [label="Inheritance\nDiagram"];
                    "uqbar.sphinx.inheritance.inheritance_diagram" [label="inheritance\ndiagram"];
                }
                "builtins.Exception" -> "uqbar.book.console.ConsoleError";
                "builtins.int" -> "enum.IntEnum";
                "builtins.object" -> "code.InteractiveInterpreter";
                "builtins.object" -> "collections.abc.Container";
                "builtins.object" -> "collections.abc.Iterable";
                "builtins.object" -> "collections.abc.Sized";
                "builtins.object" -> "docutils.nodes.Body";
                "builtins.object" -> "docutils.nodes.Node";
                "builtins.object" -> "docutils.parsers.rst.Directive";
                "builtins.object" -> "enum.Enum";
                "builtins.object" -> "uqbar.apis.builders.APIBuilder";
                "builtins.object" -> "uqbar.apis.documenters.MemberDocumenter";
                "builtins.object" -> "uqbar.apis.documenters.ModuleDocumenter";
                "builtins.object" -> "uqbar.apis.documenters.RootDocumenter";
                "builtins.object" -> "uqbar.apis.dummy.MyParentClass";
                "builtins.object" -> "uqbar.apis.graphs.InheritanceGraph";
                "builtins.object" -> "uqbar.book.console.ConsoleInput";
                "builtins.object" -> "uqbar.book.console.ConsoleOutput";
                "builtins.object" -> "uqbar.book.console.MonkeyPatch";
                "builtins.object" -> "uqbar.book.extensions.Extension";
                "builtins.object" -> "uqbar.containers.dependency_graph.DependencyGraph";
                "builtins.object" -> "uqbar.containers.unique_tree.UniqueTreeNode";
                "builtins.object" -> "uqbar.graphs.core.Edge";
                "builtins.object" -> "uqbar.graphs.graphers.Grapher";
                "builtins.object" -> "uqbar.io.DirectoryChange";
                "builtins.object" -> "uqbar.io.Profiler";
                "builtins.object" -> "uqbar.io.RedirectedStreams";
                "builtins.object" -> "uqbar.io.Timer";
                "code.InteractiveConsole" -> "uqbar.book.console.Console";
                "collections.abc.MutableMapping" -> "uqbar.graphs.attrs.Attributes";
                "docutils.nodes.Element" -> "uqbar.book.sphinx.uqbar_book_defaults_block";
                "docutils.nodes.Element" -> "uqbar.book.sphinx.uqbar_book_import_block";
                "docutils.nodes.Element" -> "uqbar.sphinx.inheritance.inheritance_diagram";
                "docutils.nodes.General" -> "uqbar.book.sphinx.uqbar_book_defaults_block";
                "docutils.nodes.General" -> "uqbar.book.sphinx.uqbar_book_import_block";
                "docutils.nodes.General" -> "uqbar.sphinx.inheritance.inheritance_diagram";
                "docutils.parsers.rst.Directive" -> "uqbar.book.sphinx.UqbarBookDefaultsDirective";
                "docutils.parsers.rst.Directive" -> "uqbar.book.sphinx.UqbarBookDirective";
                "docutils.parsers.rst.Directive" -> "uqbar.book.sphinx.UqbarBookImportDirective";
                "docutils.parsers.rst.Directive" -> "uqbar.sphinx.inheritance.InheritanceDiagram";
                "enum.Enum" -> "uqbar.enums.StrictEnumeration";
                "enum.IntEnum" -> "uqbar.enums.IntEnumeration";
                "uqbar.apis.documenters.ClassDocumenter" -> "uqbar.apis.summarizers.SummarizingClassDocumenter";
                "uqbar.apis.documenters.ModuleDocumenter" -> "uqbar.apis.summarizers.ImmaterialModuleDocumenter";
                "uqbar.apis.documenters.ModuleDocumenter" -> "uqbar.apis.summarizers.SummarizingModuleDocumenter";
                "uqbar.apis.documenters.RootDocumenter" -> "uqbar.apis.summarizers.SummarizingRootDocumenter";
                "uqbar.containers.unique_tree.UniqueTreeList" -> "uqbar.apis.nodes.PackageNode";
                "uqbar.containers.unique_tree.UniqueTreeList" -> "uqbar.graphs.core.Graph";
                "uqbar.containers.unique_tree.UniqueTreeList" -> "uqbar.graphs.core.Node";
                "uqbar.containers.unique_tree.UniqueTreeList" -> "uqbar.graphs.html.Table";
                "uqbar.containers.unique_tree.UniqueTreeList" -> "uqbar.graphs.html.TableCell";
                "uqbar.containers.unique_tree.UniqueTreeList" -> "uqbar.graphs.html.TableRow";
                "uqbar.containers.unique_tree.UniqueTreeList" -> "uqbar.graphs.records.RecordGroup";
                "uqbar.containers.unique_tree.UniqueTreeNode" -> "uqbar.apis.nodes.ModuleNode";
                "uqbar.containers.unique_tree.UniqueTreeNode" -> "uqbar.graphs.core.Attachable";
                "uqbar.containers.unique_tree.UniqueTreeNode" -> "uqbar.graphs.html.HRule";
                "uqbar.containers.unique_tree.UniqueTreeNode" -> "uqbar.graphs.html.LineBreak";
                "uqbar.containers.unique_tree.UniqueTreeNode" -> "uqbar.graphs.html.Text";
                "uqbar.containers.unique_tree.UniqueTreeNode" -> "uqbar.graphs.html.VRule";
                "uqbar.containers.unique_tree.UniqueTreeNode" -> "uqbar.graphs.records.RecordField";
                "uqbar.graphs.core.Attachable" -> "uqbar.graphs.html.TableCell";
                "uqbar.graphs.core.Attachable" -> "uqbar.graphs.records.RecordField";
            }
        """
    )
    pickle.dumps(inheritance_graph)


@pytest.mark.xfail(
    sys.version_info.minor < 11, reason="ReprEnum introduced in 3.11", strict=True
)
def test_03_py311():
    inheritance_graph = uqbar.apis.InheritanceGraph(
        package_paths=["uqbar"], lineage_paths=["uqbar"]
    )
    assert str(inheritance_graph) == uqbar.strings.normalize(
        r"""
            digraph InheritanceGraph {
                graph [bgcolor=transparent,
                    color=lightsteelblue2,
                    fontname=Arial,
                    fontsize=10,
                    outputorder=edgesfirst,
                    overlap=prism,
                    penwidth=2,
                    rankdir=LR,
                    splines=spline,
                    style="dashed, rounded",
                    truecolor=true];
                node [colorscheme=pastel19,
                    fontname=Arial,
                    fontsize=10,
                    height=0,
                    penwidth=2,
                    shape=box,
                    style="filled, rounded",
                    width=0];
                edge [color=lightslategrey,
                    penwidth=1];
                subgraph cluster_builtins {
                    graph [label=builtins];
                    node [color=1];
                    "builtins.BaseException" [label="Base\nException"];
                    "builtins.Exception" [label=Exception];
                    "builtins.int" [label=int];
                    "builtins.object" [label=object];
                    "builtins.BaseException" -> "builtins.Exception";
                    "builtins.object" -> "builtins.BaseException";
                    "builtins.object" -> "builtins.int";
                }
                subgraph cluster_code {
                    graph [label=code];
                    node [color=2];
                    "code.InteractiveConsole" [label="Interactive\nConsole"];
                    "code.InteractiveInterpreter" [label="Interactive\nInterpreter"];
                    "code.InteractiveInterpreter" -> "code.InteractiveConsole";
                }
                subgraph "cluster_collections.abc" {
                    graph [label="collections.abc"];
                    node [color=3];
                    "collections.abc.Collection" [label=Collection,
                        shape=oval,
                        style=bold];
                    "collections.abc.Container" [label=Container,
                        shape=oval,
                        style=bold];
                    "collections.abc.Iterable" [label=Iterable,
                        shape=oval,
                        style=bold];
                    "collections.abc.Mapping" [label=Mapping,
                        shape=oval,
                        style=bold];
                    "collections.abc.MutableMapping" [label="Mutable\nMapping",
                        shape=oval,
                        style=bold];
                    "collections.abc.Sized" [label=Sized,
                        shape=oval,
                        style=bold];
                    "collections.abc.Collection" -> "collections.abc.Mapping";
                    "collections.abc.Container" -> "collections.abc.Collection";
                    "collections.abc.Iterable" -> "collections.abc.Collection";
                    "collections.abc.Mapping" -> "collections.abc.MutableMapping";
                    "collections.abc.Sized" -> "collections.abc.Collection";
                }
                subgraph "cluster_docutils.nodes" {
                    graph [label="docutils.nodes"];
                    node [color=4];
                    "docutils.nodes.Body" [label=Body];
                    "docutils.nodes.Element" [label=Element];
                    "docutils.nodes.General" [label=General];
                    "docutils.nodes.Node" [label="Node"];
                    "docutils.nodes.Body" -> "docutils.nodes.General";
                    "docutils.nodes.Node" -> "docutils.nodes.Element";
                }
                subgraph "cluster_docutils.parsers.rst" {
                    graph [label="docutils.parsers.rst"];
                    node [color=5];
                    "docutils.parsers.rst.Directive" [label=Directive];
                }
                subgraph cluster_enum {
                    graph [label=enum];
                    node [color=6];
                    "enum.Enum" [label=Enum];
                    "enum.IntEnum" [label="Int\nEnum"];
                    "enum.ReprEnum" [label="Repr\nEnum"];
                    "enum.Enum" -> "enum.ReprEnum";
                    "enum.ReprEnum" -> "enum.IntEnum";
                }
                subgraph "cluster_uqbar.apis.builders" {
                    graph [label="uqbar.apis.builders"];
                    node [color=7];
                    "uqbar.apis.builders.APIBuilder" [label=APIBuilder];
                }
                subgraph "cluster_uqbar.apis.documenters" {
                    graph [label="uqbar.apis.documenters"];
                    node [color=8];
                    "uqbar.apis.documenters.ClassDocumenter" [label="Class\nDocumenter"];
                    "uqbar.apis.documenters.FunctionDocumenter" [label="Function\nDocumenter"];
                    "uqbar.apis.documenters.MemberDocumenter" [label="Member\nDocumenter"];
                    "uqbar.apis.documenters.ModuleDocumenter" [label="Module\nDocumenter"];
                    "uqbar.apis.documenters.RootDocumenter" [label="Root\nDocumenter"];
                    "uqbar.apis.documenters.MemberDocumenter" -> "uqbar.apis.documenters.ClassDocumenter";
                    "uqbar.apis.documenters.MemberDocumenter" -> "uqbar.apis.documenters.FunctionDocumenter";
                }
                subgraph "cluster_uqbar.apis.dummy" {
                    graph [label="uqbar.apis.dummy"];
                    node [color=9];
                    "uqbar.apis.dummy.MyChildClass" [label="My\nChild\nClass"];
                    "uqbar.apis.dummy.MyParentClass" [label="My\nParent\nClass"];
                    "uqbar.apis.dummy.MyParentClass" -> "uqbar.apis.dummy.MyChildClass";
                }
                subgraph "cluster_uqbar.apis.graphs" {
                    graph [label="uqbar.apis.graphs"];
                    node [color=1];
                    "uqbar.apis.graphs.InheritanceGraph" [label="Inheritance\nGraph"];
                }
                subgraph "cluster_uqbar.apis.nodes" {
                    graph [label="uqbar.apis.nodes"];
                    node [color=2];
                    "uqbar.apis.nodes.ModuleNode" [label="Module\nNode"];
                    "uqbar.apis.nodes.PackageNode" [label="Package\nNode"];
                }
                subgraph "cluster_uqbar.apis.summarizers" {
                    graph [label="uqbar.apis.summarizers"];
                    node [color=3];
                    "uqbar.apis.summarizers.ImmaterialClassDocumenter" [label="Immaterial\nClass\nDocumenter"];
                    "uqbar.apis.summarizers.ImmaterialModuleDocumenter" [label="Immaterial\nModule\nDocumenter"];
                    "uqbar.apis.summarizers.SummarizingClassDocumenter" [label="Summarizing\nClass\nDocumenter"];
                    "uqbar.apis.summarizers.SummarizingModuleDocumenter" [label="Summarizing\nModule\nDocumenter"];
                    "uqbar.apis.summarizers.SummarizingRootDocumenter" [label="Summarizing\nRoot\nDocumenter"];
                    "uqbar.apis.summarizers.SummarizingClassDocumenter" -> "uqbar.apis.summarizers.ImmaterialClassDocumenter";
                }
                subgraph "cluster_uqbar.book.console" {
                    graph [label="uqbar.book.console"];
                    node [color=4];
                    "uqbar.book.console.Console" [label=Console];
                    "uqbar.book.console.ConsoleError" [label="Console\nError"];
                    "uqbar.book.console.ConsoleInput" [label="Console\nInput"];
                    "uqbar.book.console.ConsoleOutput" [label="Console\nOutput"];
                    "uqbar.book.console.MonkeyPatch" [label="Monkey\nPatch"];
                }
                subgraph "cluster_uqbar.book.extensions" {
                    graph [label="uqbar.book.extensions"];
                    node [color=5];
                    "uqbar.book.extensions.Extension" [label=Extension];
                    "uqbar.book.extensions.GraphExtension" [label="Graph\nExtension"];
                    "uqbar.book.extensions.Extension" -> "uqbar.book.extensions.GraphExtension";
                }
                subgraph "cluster_uqbar.book.sphinx" {
                    graph [label="uqbar.book.sphinx"];
                    node [color=6];
                    "uqbar.book.sphinx.UqbarBookDefaultsDirective" [label="Uqbar\nBook\nDefaults\nDirective"];
                    "uqbar.book.sphinx.UqbarBookDirective" [label="Uqbar\nBook\nDirective"];
                    "uqbar.book.sphinx.UqbarBookImportDirective" [label="Uqbar\nBook\nImport\nDirective"];
                    "uqbar.book.sphinx.uqbar_book_defaults_block" [label="uqbar\nbook\ndefaults\nblock"];
                    "uqbar.book.sphinx.uqbar_book_import_block" [label="uqbar\nbook\nimport\nblock"];
                }
                subgraph "cluster_uqbar.containers.dependency_graph" {
                    graph [label="uqbar.containers.dependency_graph"];
                    node [color=7];
                    "uqbar.containers.dependency_graph.DependencyGraph" [label="Dependency\nGraph"];
                }
                subgraph "cluster_uqbar.containers.unique_tree" {
                    graph [label="uqbar.containers.unique_tree"];
                    node [color=8];
                    "uqbar.containers.unique_tree.UniqueTreeContainer" [label="Unique\nTree\nContainer"];
                    "uqbar.containers.unique_tree.UniqueTreeDict" [label="Unique\nTree\nDict"];
                    "uqbar.containers.unique_tree.UniqueTreeList" [label="Unique\nTree\nList"];
                    "uqbar.containers.unique_tree.UniqueTreeNode" [label="Unique\nTree\nNode"];
                    "uqbar.containers.unique_tree.UniqueTreeSet" [label="Unique\nTree\nSet"];
                    "uqbar.containers.unique_tree.UniqueTreeTuple" [label="Unique\nTree\nTuple"];
                    "uqbar.containers.unique_tree.UniqueTreeContainer" -> "uqbar.containers.unique_tree.UniqueTreeDict";
                    "uqbar.containers.unique_tree.UniqueTreeContainer" -> "uqbar.containers.unique_tree.UniqueTreeList";
                    "uqbar.containers.unique_tree.UniqueTreeContainer" -> "uqbar.containers.unique_tree.UniqueTreeSet";
                    "uqbar.containers.unique_tree.UniqueTreeContainer" -> "uqbar.containers.unique_tree.UniqueTreeTuple";
                    "uqbar.containers.unique_tree.UniqueTreeNode" -> "uqbar.containers.unique_tree.UniqueTreeContainer";
                }
                subgraph "cluster_uqbar.enums" {
                    graph [label="uqbar.enums"];
                    node [color=9];
                    "uqbar.enums.IntEnumeration" [label="Int\nEnumeration"];
                    "uqbar.enums.StrictEnumeration" [label="Strict\nEnumeration"];
                }
                subgraph "cluster_uqbar.graphs.attrs" {
                    graph [label="uqbar.graphs.attrs"];
                    node [color=1];
                    "uqbar.graphs.attrs.Attributes" [label=Attributes];
                }
                subgraph "cluster_uqbar.graphs.core" {
                    graph [label="uqbar.graphs.core"];
                    node [color=2];
                    "uqbar.graphs.core.Attachable" [label=Attachable];
                    "uqbar.graphs.core.Edge" [label="Edge"];
                    "uqbar.graphs.core.Graph" [label="Graph"];
                    "uqbar.graphs.core.Node" [label="Node"];
                }
                subgraph "cluster_uqbar.graphs.graphers" {
                    graph [label="uqbar.graphs.graphers"];
                    node [color=3];
                    "uqbar.graphs.graphers.Grapher" [label=Grapher];
                }
                subgraph "cluster_uqbar.graphs.html" {
                    graph [label="uqbar.graphs.html"];
                    node [color=4];
                    "uqbar.graphs.html.HRule" [label=HRule];
                    "uqbar.graphs.html.LineBreak" [label="Line\nBreak"];
                    "uqbar.graphs.html.Table" [label=Table];
                    "uqbar.graphs.html.TableCell" [label="Table\nCell"];
                    "uqbar.graphs.html.TableRow" [label="Table\nRow"];
                    "uqbar.graphs.html.Text" [label=Text];
                    "uqbar.graphs.html.VRule" [label=VRule];
                }
                subgraph "cluster_uqbar.graphs.records" {
                    graph [label="uqbar.graphs.records"];
                    node [color=5];
                    "uqbar.graphs.records.RecordField" [label="Record\nField"];
                    "uqbar.graphs.records.RecordGroup" [label="Record\nGroup"];
                }
                subgraph "cluster_uqbar.io" {
                    graph [label="uqbar.io"];
                    node [color=6];
                    "uqbar.io.DirectoryChange" [color=black,
                        fontcolor=white,
                        label="Directory\nChange"];
                    "uqbar.io.Profiler" [color=black,
                        fontcolor=white,
                        label=Profiler];
                    "uqbar.io.RedirectedStreams" [color=black,
                        fontcolor=white,
                        label="Redirected\nStreams"];
                    "uqbar.io.Timer" [color=black,
                        fontcolor=white,
                        label=Timer];
                }
                subgraph "cluster_uqbar.sphinx.inheritance" {
                    graph [label="uqbar.sphinx.inheritance"];
                    node [color=7];
                    "uqbar.sphinx.inheritance.InheritanceDiagram" [label="Inheritance\nDiagram"];
                    "uqbar.sphinx.inheritance.inheritance_diagram" [label="inheritance\ndiagram"];
                }
                "builtins.Exception" -> "uqbar.book.console.ConsoleError";
                "builtins.int" -> "enum.IntEnum";
                "builtins.object" -> "code.InteractiveInterpreter";
                "builtins.object" -> "collections.abc.Container";
                "builtins.object" -> "collections.abc.Iterable";
                "builtins.object" -> "collections.abc.Sized";
                "builtins.object" -> "docutils.nodes.Body";
                "builtins.object" -> "docutils.nodes.Node";
                "builtins.object" -> "docutils.parsers.rst.Directive";
                "builtins.object" -> "enum.Enum";
                "builtins.object" -> "uqbar.apis.builders.APIBuilder";
                "builtins.object" -> "uqbar.apis.documenters.MemberDocumenter";
                "builtins.object" -> "uqbar.apis.documenters.ModuleDocumenter";
                "builtins.object" -> "uqbar.apis.documenters.RootDocumenter";
                "builtins.object" -> "uqbar.apis.dummy.MyParentClass";
                "builtins.object" -> "uqbar.apis.graphs.InheritanceGraph";
                "builtins.object" -> "uqbar.book.console.ConsoleInput";
                "builtins.object" -> "uqbar.book.console.ConsoleOutput";
                "builtins.object" -> "uqbar.book.console.MonkeyPatch";
                "builtins.object" -> "uqbar.book.extensions.Extension";
                "builtins.object" -> "uqbar.containers.dependency_graph.DependencyGraph";
                "builtins.object" -> "uqbar.containers.unique_tree.UniqueTreeNode";
                "builtins.object" -> "uqbar.graphs.core.Edge";
                "builtins.object" -> "uqbar.graphs.graphers.Grapher";
                "builtins.object" -> "uqbar.io.DirectoryChange";
                "builtins.object" -> "uqbar.io.Profiler";
                "builtins.object" -> "uqbar.io.RedirectedStreams";
                "builtins.object" -> "uqbar.io.Timer";
                "code.InteractiveConsole" -> "uqbar.book.console.Console";
                "collections.abc.MutableMapping" -> "uqbar.graphs.attrs.Attributes";
                "docutils.nodes.Element" -> "uqbar.book.sphinx.uqbar_book_defaults_block";
                "docutils.nodes.Element" -> "uqbar.book.sphinx.uqbar_book_import_block";
                "docutils.nodes.Element" -> "uqbar.sphinx.inheritance.inheritance_diagram";
                "docutils.nodes.General" -> "uqbar.book.sphinx.uqbar_book_defaults_block";
                "docutils.nodes.General" -> "uqbar.book.sphinx.uqbar_book_import_block";
                "docutils.nodes.General" -> "uqbar.sphinx.inheritance.inheritance_diagram";
                "docutils.parsers.rst.Directive" -> "uqbar.book.sphinx.UqbarBookDefaultsDirective";
                "docutils.parsers.rst.Directive" -> "uqbar.book.sphinx.UqbarBookDirective";
                "docutils.parsers.rst.Directive" -> "uqbar.book.sphinx.UqbarBookImportDirective";
                "docutils.parsers.rst.Directive" -> "uqbar.sphinx.inheritance.InheritanceDiagram";
                "enum.Enum" -> "uqbar.enums.StrictEnumeration";
                "enum.IntEnum" -> "uqbar.enums.IntEnumeration";
                "uqbar.apis.documenters.ClassDocumenter" -> "uqbar.apis.summarizers.SummarizingClassDocumenter";
                "uqbar.apis.documenters.ModuleDocumenter" -> "uqbar.apis.summarizers.ImmaterialModuleDocumenter";
                "uqbar.apis.documenters.ModuleDocumenter" -> "uqbar.apis.summarizers.SummarizingModuleDocumenter";
                "uqbar.apis.documenters.RootDocumenter" -> "uqbar.apis.summarizers.SummarizingRootDocumenter";
                "uqbar.containers.unique_tree.UniqueTreeList" -> "uqbar.apis.nodes.PackageNode";
                "uqbar.containers.unique_tree.UniqueTreeList" -> "uqbar.graphs.core.Graph";
                "uqbar.containers.unique_tree.UniqueTreeList" -> "uqbar.graphs.core.Node";
                "uqbar.containers.unique_tree.UniqueTreeList" -> "uqbar.graphs.html.Table";
                "uqbar.containers.unique_tree.UniqueTreeList" -> "uqbar.graphs.html.TableCell";
                "uqbar.containers.unique_tree.UniqueTreeList" -> "uqbar.graphs.html.TableRow";
                "uqbar.containers.unique_tree.UniqueTreeList" -> "uqbar.graphs.records.RecordGroup";
                "uqbar.containers.unique_tree.UniqueTreeNode" -> "uqbar.apis.nodes.ModuleNode";
                "uqbar.containers.unique_tree.UniqueTreeNode" -> "uqbar.graphs.core.Attachable";
                "uqbar.containers.unique_tree.UniqueTreeNode" -> "uqbar.graphs.html.HRule";
                "uqbar.containers.unique_tree.UniqueTreeNode" -> "uqbar.graphs.html.LineBreak";
                "uqbar.containers.unique_tree.UniqueTreeNode" -> "uqbar.graphs.html.Text";
                "uqbar.containers.unique_tree.UniqueTreeNode" -> "uqbar.graphs.html.VRule";
                "uqbar.containers.unique_tree.UniqueTreeNode" -> "uqbar.graphs.records.RecordField";
                "uqbar.graphs.core.Attachable" -> "uqbar.graphs.html.TableCell";
                "uqbar.graphs.core.Attachable" -> "uqbar.graphs.records.RecordField";
            }
        """
    )
    pickle.dumps(inheritance_graph)


def test_04():
    inheritance_graph = uqbar.apis.InheritanceGraph(
        package_paths=["uqbar"], lineage_paths=["uqbar.apis.dummy"]
    )
    assert inheritance_graph.parents_to_children == collections.OrderedDict(
        [
            ("builtins.object", ["uqbar.apis.dummy.MyParentClass"]),
            ("uqbar.apis.dummy.MyParentClass", ["uqbar.apis.dummy.MyChildClass"]),
        ]
    )
    assert str(inheritance_graph) == uqbar.strings.normalize(
        r"""
        digraph InheritanceGraph {
            graph [bgcolor=transparent,
                color=lightsteelblue2,
                fontname=Arial,
                fontsize=10,
                outputorder=edgesfirst,
                overlap=prism,
                penwidth=2,
                rankdir=LR,
                splines=spline,
                style="dashed, rounded",
                truecolor=true];
            node [colorscheme=pastel19,
                fontname=Arial,
                fontsize=10,
                height=0,
                penwidth=2,
                shape=box,
                style="filled, rounded",
                width=0];
            edge [color=lightslategrey,
                penwidth=1];
            subgraph cluster_builtins {
                graph [label=builtins];
                node [color=1];
                "builtins.object" [label=object];
            }
            subgraph "cluster_uqbar.apis.dummy" {
                graph [label="uqbar.apis.dummy"];
                node [color=2];
                "uqbar.apis.dummy.MyChildClass" [color=black,
                    fontcolor=white,
                    label="My\nChild\nClass"];
                "uqbar.apis.dummy.MyParentClass" [color=black,
                    fontcolor=white,
                    label="My\nParent\nClass"];
                "uqbar.apis.dummy.MyParentClass" -> "uqbar.apis.dummy.MyChildClass";
            }
            "builtins.object" -> "uqbar.apis.dummy.MyParentClass";
        }
    """
    )
    pickle.dumps(inheritance_graph)
    pickle.dumps(uqbar.apis.dummy.MyChildClass)
    with pytest.raises(AttributeError):
        pickle.dumps(uqbar.apis.dummy.MyParentClass)
