import abc
import collections
import enum
import docutils.nodes
import uqbar.apis
import uqbar.strings


def test_01():
    inheritance_graph = uqbar.apis.InheritanceGraph(
        package_paths=['uqbar.containers'],
        )
    assert inheritance_graph.parents_to_children == collections.OrderedDict([
        (object, [
            uqbar.containers.DependencyGraph,
            uqbar.containers.UniqueTreeNode,
        ]),
        (uqbar.containers.UniqueTreeNode, [uqbar.containers.UniqueTreeContainer]),
    ])
    assert str(inheritance_graph) == uqbar.strings.normalize(r'''
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
            subgraph "cluster_uqbar.containers" {
                graph [label="uqbar.containers"];
                node [color=2];
                "uqbar.containers.DependencyGraph.DependencyGraph" [label="Dependency\nGraph"];
                "uqbar.containers.UniqueTreeContainer.UniqueTreeContainer" [label="Unique\nTree\nContainer"];
                "uqbar.containers.UniqueTreeNode.UniqueTreeNode" [label="Unique\nTree\nNode"];
                "uqbar.containers.UniqueTreeNode.UniqueTreeNode" -> "uqbar.containers.UniqueTreeContainer.UniqueTreeContainer";
            }
            "builtins.object" -> "uqbar.containers.DependencyGraph.DependencyGraph";
            "builtins.object" -> "uqbar.containers.UniqueTreeNode.UniqueTreeNode";
        }
    ''')


def test_02():
    inheritance_graph = uqbar.apis.InheritanceGraph(
        package_paths=['uqbar'],
        lineage_paths=['uqbar.containers'],
        )
    assert inheritance_graph.parents_to_children == collections.OrderedDict([
        (object, [
            uqbar.containers.DependencyGraph,
            uqbar.containers.UniqueTreeNode,
        ]),
        (uqbar.containers.UniqueTreeContainer, [
            uqbar.apis.PackageNode,
            uqbar.graphs.Graph,
            uqbar.graphs.Node,
            uqbar.graphs.RecordGroup,
            uqbar.graphs.Table,
            uqbar.graphs.TableCell,
            uqbar.graphs.TableRow,
        ]),
        (uqbar.containers.UniqueTreeNode, [
            uqbar.apis.ModuleNode,
            uqbar.containers.UniqueTreeContainer,
            uqbar.graphs.Attachable,
            uqbar.graphs.HRule,
            uqbar.graphs.LineBreak,
            uqbar.graphs.RecordField,
            uqbar.graphs.Text,
            uqbar.graphs.VRule,
        ]),
        (uqbar.graphs.Attachable, [
            uqbar.graphs.RecordField,
            uqbar.graphs.TableCell,
        ]),
    ])
    assert str(inheritance_graph) == uqbar.strings.normalize(r'''
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
            subgraph "cluster_uqbar.apis" {
                graph [label="uqbar.apis"];
                node [color=2];
                "uqbar.apis.ModuleNode.ModuleNode" [label="Module\nNode"];
                "uqbar.apis.PackageNode.PackageNode" [label="Package\nNode"];
            }
            subgraph "cluster_uqbar.containers" {
                graph [label="uqbar.containers"];
                node [color=3];
                "uqbar.containers.DependencyGraph.DependencyGraph" [color=black,
                    fontcolor=white,
                    label="Dependency\nGraph"];
                "uqbar.containers.UniqueTreeContainer.UniqueTreeContainer" [color=black,
                    fontcolor=white,
                    label="Unique\nTree\nContainer"];
                "uqbar.containers.UniqueTreeNode.UniqueTreeNode" [color=black,
                    fontcolor=white,
                    label="Unique\nTree\nNode"];
                "uqbar.containers.UniqueTreeNode.UniqueTreeNode" -> "uqbar.containers.UniqueTreeContainer.UniqueTreeContainer";
            }
            subgraph "cluster_uqbar.graphs" {
                graph [label="uqbar.graphs"];
                node [color=4];
                "uqbar.graphs.Attachable.Attachable" [label=Attachable];
                "uqbar.graphs.Graph.Graph" [label="Graph"];
                "uqbar.graphs.HRule.HRule" [label=HRule];
                "uqbar.graphs.LineBreak.LineBreak" [label="Line\nBreak"];
                "uqbar.graphs.Node.Node" [label="Node"];
                "uqbar.graphs.RecordField.RecordField" [label="Record\nField"];
                "uqbar.graphs.RecordGroup.RecordGroup" [label="Record\nGroup"];
                "uqbar.graphs.Table.Table" [label=Table];
                "uqbar.graphs.TableCell.TableCell" [label="Table\nCell"];
                "uqbar.graphs.TableRow.TableRow" [label="Table\nRow"];
                "uqbar.graphs.Text.Text" [label=Text];
                "uqbar.graphs.VRule.VRule" [label=VRule];
                "uqbar.graphs.Attachable.Attachable" -> "uqbar.graphs.RecordField.RecordField";
                "uqbar.graphs.Attachable.Attachable" -> "uqbar.graphs.TableCell.TableCell";
            }
            "builtins.object" -> "uqbar.containers.DependencyGraph.DependencyGraph";
            "builtins.object" -> "uqbar.containers.UniqueTreeNode.UniqueTreeNode";
            "uqbar.containers.UniqueTreeContainer.UniqueTreeContainer" -> "uqbar.apis.PackageNode.PackageNode";
            "uqbar.containers.UniqueTreeContainer.UniqueTreeContainer" -> "uqbar.graphs.Graph.Graph";
            "uqbar.containers.UniqueTreeContainer.UniqueTreeContainer" -> "uqbar.graphs.Node.Node";
            "uqbar.containers.UniqueTreeContainer.UniqueTreeContainer" -> "uqbar.graphs.RecordGroup.RecordGroup";
            "uqbar.containers.UniqueTreeContainer.UniqueTreeContainer" -> "uqbar.graphs.Table.Table";
            "uqbar.containers.UniqueTreeContainer.UniqueTreeContainer" -> "uqbar.graphs.TableCell.TableCell";
            "uqbar.containers.UniqueTreeContainer.UniqueTreeContainer" -> "uqbar.graphs.TableRow.TableRow";
            "uqbar.containers.UniqueTreeNode.UniqueTreeNode" -> "uqbar.apis.ModuleNode.ModuleNode";
            "uqbar.containers.UniqueTreeNode.UniqueTreeNode" -> "uqbar.graphs.Attachable.Attachable";
            "uqbar.containers.UniqueTreeNode.UniqueTreeNode" -> "uqbar.graphs.HRule.HRule";
            "uqbar.containers.UniqueTreeNode.UniqueTreeNode" -> "uqbar.graphs.LineBreak.LineBreak";
            "uqbar.containers.UniqueTreeNode.UniqueTreeNode" -> "uqbar.graphs.RecordField.RecordField";
            "uqbar.containers.UniqueTreeNode.UniqueTreeNode" -> "uqbar.graphs.Text.Text";
            "uqbar.containers.UniqueTreeNode.UniqueTreeNode" -> "uqbar.graphs.VRule.VRule";
        }
    ''')


def test_03():
    inheritance_graph = uqbar.apis.InheritanceGraph(
        package_paths=['uqbar'],
        lineage_paths=['uqbar'],
        )
    assert inheritance_graph.parents_to_children == collections.OrderedDict([
        (abc.ABC, [uqbar.cli.CLI]),
        (int, [enum.IntEnum]),
        (object, [
            abc.ABC,
            int,
            collections.abc.Container,
            collections.abc.Iterable,
            collections.abc.Sized,
            docutils.nodes.Body,
            docutils.nodes.Node,
            docutils.parsers.rst.Directive,
            enum.Enum,
            uqbar.apis.APIBuilder,
            uqbar.apis.InheritanceGraph,
            uqbar.apis.MemberDocumenter,
            uqbar.apis.ModuleDocumenter,
            uqbar.apis.RootDocumenter,
            uqbar.containers.DependencyGraph,
            uqbar.containers.UniqueTreeNode,
            uqbar.graphs.Edge,
            uqbar.io.DirectoryChange,
            uqbar.io.Profiler,
            uqbar.io.RedirectedStreams,
            uqbar.io.Timer,
        ]),
        (collections.abc.Collection, [collections.abc.Mapping]),
        (collections.abc.Container, [collections.abc.Collection]),
        (collections.abc.Iterable, [collections.abc.Collection]),
        (collections.abc.Mapping, [collections.abc.MutableMapping]),
        (collections.abc.MutableMapping, [uqbar.graphs.Attributes]),
        (collections.abc.Sized, [collections.abc.Collection]),
        (docutils.nodes.Body, [docutils.nodes.General]),
        (docutils.nodes.Element, [uqbar.sphinx.inheritance.inheritance_diagram]),
        (docutils.nodes.General, [uqbar.sphinx.inheritance.inheritance_diagram]),
        (docutils.nodes.Node, [docutils.nodes.Element]),
        (docutils.parsers.rst.Directive, [uqbar.sphinx.inheritance.InheritanceDiagram]),
        (enum.Enum, [
            enum.IntEnum,
            uqbar.enums.StrictEnumeration,
        ]),
        (enum.IntEnum, [uqbar.enums.IntEnumeration]),
        (uqbar.apis.ClassDocumenter, [uqbar.apis.SummarizingClassDocumenter]),
        (uqbar.apis.MemberDocumenter, [
            uqbar.apis.ClassDocumenter,
            uqbar.apis.FunctionDocumenter,
        ]),
        (uqbar.apis.ModuleDocumenter, [uqbar.apis.SummarizingModuleDocumenter]),
        (uqbar.apis.RootDocumenter, [uqbar.apis.SummarizingRootDocumenter]),
        (uqbar.cli.CLI, [uqbar.cli.CLIAggregator]),
        (uqbar.containers.UniqueTreeContainer, [
            uqbar.apis.PackageNode,
            uqbar.graphs.Graph,
            uqbar.graphs.Node,
            uqbar.graphs.RecordGroup,
            uqbar.graphs.Table,
            uqbar.graphs.TableCell,
            uqbar.graphs.TableRow,
        ]),
        (uqbar.containers.UniqueTreeNode, [
            uqbar.apis.ModuleNode,
            uqbar.containers.UniqueTreeContainer,
            uqbar.graphs.Attachable,
            uqbar.graphs.HRule,
            uqbar.graphs.LineBreak,
            uqbar.graphs.RecordField,
            uqbar.graphs.Text,
            uqbar.graphs.VRule,
        ]),
        (uqbar.graphs.Attachable, [
            uqbar.graphs.RecordField,
            uqbar.graphs.TableCell,
        ]),
    ])
    assert str(inheritance_graph) == uqbar.strings.normalize(r'''
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
            subgraph cluster_abc {
                graph [label=abc];
                node [color=1];
                "abc.ABC" [label=ABC];
            }
            subgraph cluster_builtins {
                graph [label=builtins];
                node [color=2];
                "builtins.int" [label=int];
                "builtins.object" [label=object];
                "builtins.object" -> "builtins.int";
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
            subgraph "cluster_uqbar.apis" {
                graph [label="uqbar.apis"];
                node [color=7];
                "uqbar.apis.APIBuilder.APIBuilder" [label=APIBuilder];
                "uqbar.apis.ClassDocumenter.ClassDocumenter" [label="Class\nDocumenter"];
                "uqbar.apis.FunctionDocumenter.FunctionDocumenter" [label="Function\nDocumenter"];
                "uqbar.apis.InheritanceGraph.InheritanceGraph" [label="Inheritance\nGraph"];
                "uqbar.apis.MemberDocumenter.MemberDocumenter" [label="Member\nDocumenter",
                    shape=oval,
                    style=bold];
                "uqbar.apis.ModuleDocumenter.ModuleDocumenter" [label="Module\nDocumenter"];
                "uqbar.apis.ModuleNode.ModuleNode" [label="Module\nNode"];
                "uqbar.apis.PackageNode.PackageNode" [label="Package\nNode"];
                "uqbar.apis.RootDocumenter.RootDocumenter" [label="Root\nDocumenter"];
                "uqbar.apis.SummarizingClassDocumenter.SummarizingClassDocumenter" [label="Summarizing\nClass\nDocumenter"];
                "uqbar.apis.SummarizingModuleDocumenter.SummarizingModuleDocumenter" [label="Summarizing\nModule\nDocumenter"];
                "uqbar.apis.SummarizingRootDocumenter.SummarizingRootDocumenter" [label="Summarizing\nRoot\nDocumenter"];
                "uqbar.apis.ClassDocumenter.ClassDocumenter" -> "uqbar.apis.SummarizingClassDocumenter.SummarizingClassDocumenter";
                "uqbar.apis.MemberDocumenter.MemberDocumenter" -> "uqbar.apis.ClassDocumenter.ClassDocumenter";
                "uqbar.apis.MemberDocumenter.MemberDocumenter" -> "uqbar.apis.FunctionDocumenter.FunctionDocumenter";
                "uqbar.apis.ModuleDocumenter.ModuleDocumenter" -> "uqbar.apis.SummarizingModuleDocumenter.SummarizingModuleDocumenter";
                "uqbar.apis.RootDocumenter.RootDocumenter" -> "uqbar.apis.SummarizingRootDocumenter.SummarizingRootDocumenter";
            }
            subgraph "cluster_uqbar.cli" {
                graph [label="uqbar.cli"];
                node [color=8];
                "uqbar.cli.CLI.CLI" [label=CLI,
                    shape=oval,
                    style=bold];
                "uqbar.cli.CLIAggregator.CLIAggregator" [label=CLIAggregator];
                "uqbar.cli.CLI.CLI" -> "uqbar.cli.CLIAggregator.CLIAggregator";
            }
            subgraph "cluster_uqbar.containers" {
                graph [label="uqbar.containers"];
                node [color=9];
                "uqbar.containers.DependencyGraph.DependencyGraph" [label="Dependency\nGraph"];
                "uqbar.containers.UniqueTreeContainer.UniqueTreeContainer" [label="Unique\nTree\nContainer"];
                "uqbar.containers.UniqueTreeNode.UniqueTreeNode" [label="Unique\nTree\nNode"];
                "uqbar.containers.UniqueTreeNode.UniqueTreeNode" -> "uqbar.containers.UniqueTreeContainer.UniqueTreeContainer";
            }
            subgraph "cluster_uqbar.enums" {
                graph [label="uqbar.enums"];
                node [color=1];
                "uqbar.enums.IntEnumeration" [label="Int\nEnumeration"];
                "uqbar.enums.StrictEnumeration" [label="Strict\nEnumeration"];
            }
            subgraph "cluster_uqbar.graphs" {
                graph [label="uqbar.graphs"];
                node [color=2];
                "uqbar.graphs.Attachable.Attachable" [label=Attachable];
                "uqbar.graphs.Attributes.Attributes" [label=Attributes];
                "uqbar.graphs.Edge.Edge" [label="Edge"];
                "uqbar.graphs.Graph.Graph" [label="Graph"];
                "uqbar.graphs.HRule.HRule" [label=HRule];
                "uqbar.graphs.LineBreak.LineBreak" [label="Line\nBreak"];
                "uqbar.graphs.Node.Node" [label="Node"];
                "uqbar.graphs.RecordField.RecordField" [label="Record\nField"];
                "uqbar.graphs.RecordGroup.RecordGroup" [label="Record\nGroup"];
                "uqbar.graphs.Table.Table" [label=Table];
                "uqbar.graphs.TableCell.TableCell" [label="Table\nCell"];
                "uqbar.graphs.TableRow.TableRow" [label="Table\nRow"];
                "uqbar.graphs.Text.Text" [label=Text];
                "uqbar.graphs.VRule.VRule" [label=VRule];
                "uqbar.graphs.Attachable.Attachable" -> "uqbar.graphs.RecordField.RecordField";
                "uqbar.graphs.Attachable.Attachable" -> "uqbar.graphs.TableCell.TableCell";
            }
            subgraph "cluster_uqbar.io" {
                graph [label="uqbar.io"];
                node [color=3];
                "uqbar.io.DirectoryChange.DirectoryChange" [label="Directory\nChange"];
                "uqbar.io.Profiler.Profiler" [label=Profiler];
                "uqbar.io.RedirectedStreams.RedirectedStreams" [label="Redirected\nStreams"];
                "uqbar.io.Timer.Timer" [label=Timer];
            }
            subgraph "cluster_uqbar.sphinx.inheritance" {
                graph [label="uqbar.sphinx.inheritance"];
                node [color=4];
                "uqbar.sphinx.inheritance.InheritanceDiagram" [label="Inheritance\nDiagram"];
                "uqbar.sphinx.inheritance.inheritance_diagram" [label="inheritance\ndiagram"];
            }
            "abc.ABC" -> "uqbar.cli.CLI.CLI";
            "builtins.int" -> "enum.IntEnum";
            "builtins.object" -> "abc.ABC";
            "builtins.object" -> "collections.abc.Container";
            "builtins.object" -> "collections.abc.Iterable";
            "builtins.object" -> "collections.abc.Sized";
            "builtins.object" -> "docutils.nodes.Body";
            "builtins.object" -> "docutils.nodes.Node";
            "builtins.object" -> "docutils.parsers.rst.Directive";
            "builtins.object" -> "enum.Enum";
            "builtins.object" -> "uqbar.apis.APIBuilder.APIBuilder";
            "builtins.object" -> "uqbar.apis.InheritanceGraph.InheritanceGraph";
            "builtins.object" -> "uqbar.apis.MemberDocumenter.MemberDocumenter";
            "builtins.object" -> "uqbar.apis.ModuleDocumenter.ModuleDocumenter";
            "builtins.object" -> "uqbar.apis.RootDocumenter.RootDocumenter";
            "builtins.object" -> "uqbar.containers.DependencyGraph.DependencyGraph";
            "builtins.object" -> "uqbar.containers.UniqueTreeNode.UniqueTreeNode";
            "builtins.object" -> "uqbar.graphs.Edge.Edge";
            "builtins.object" -> "uqbar.io.DirectoryChange.DirectoryChange";
            "builtins.object" -> "uqbar.io.Profiler.Profiler";
            "builtins.object" -> "uqbar.io.RedirectedStreams.RedirectedStreams";
            "builtins.object" -> "uqbar.io.Timer.Timer";
            "collections.abc.MutableMapping" -> "uqbar.graphs.Attributes.Attributes";
            "docutils.nodes.Element" -> "uqbar.sphinx.inheritance.inheritance_diagram";
            "docutils.nodes.General" -> "uqbar.sphinx.inheritance.inheritance_diagram";
            "docutils.parsers.rst.Directive" -> "uqbar.sphinx.inheritance.InheritanceDiagram";
            "enum.Enum" -> "uqbar.enums.StrictEnumeration";
            "enum.IntEnum" -> "uqbar.enums.IntEnumeration";
            "uqbar.containers.UniqueTreeContainer.UniqueTreeContainer" -> "uqbar.apis.PackageNode.PackageNode";
            "uqbar.containers.UniqueTreeContainer.UniqueTreeContainer" -> "uqbar.graphs.Graph.Graph";
            "uqbar.containers.UniqueTreeContainer.UniqueTreeContainer" -> "uqbar.graphs.Node.Node";
            "uqbar.containers.UniqueTreeContainer.UniqueTreeContainer" -> "uqbar.graphs.RecordGroup.RecordGroup";
            "uqbar.containers.UniqueTreeContainer.UniqueTreeContainer" -> "uqbar.graphs.Table.Table";
            "uqbar.containers.UniqueTreeContainer.UniqueTreeContainer" -> "uqbar.graphs.TableCell.TableCell";
            "uqbar.containers.UniqueTreeContainer.UniqueTreeContainer" -> "uqbar.graphs.TableRow.TableRow";
            "uqbar.containers.UniqueTreeNode.UniqueTreeNode" -> "uqbar.apis.ModuleNode.ModuleNode";
            "uqbar.containers.UniqueTreeNode.UniqueTreeNode" -> "uqbar.graphs.Attachable.Attachable";
            "uqbar.containers.UniqueTreeNode.UniqueTreeNode" -> "uqbar.graphs.HRule.HRule";
            "uqbar.containers.UniqueTreeNode.UniqueTreeNode" -> "uqbar.graphs.LineBreak.LineBreak";
            "uqbar.containers.UniqueTreeNode.UniqueTreeNode" -> "uqbar.graphs.RecordField.RecordField";
            "uqbar.containers.UniqueTreeNode.UniqueTreeNode" -> "uqbar.graphs.Text.Text";
            "uqbar.containers.UniqueTreeNode.UniqueTreeNode" -> "uqbar.graphs.VRule.VRule";
        }
    ''')
