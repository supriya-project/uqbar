import collections
import importlib
import inspect
import types
import uqbar.graphs
import uqbar.strings
from typing import (  # noqa
    Any, Dict, List, Mapping, MutableMapping, Sequence, Set, Tuple, Union
    )


class InheritanceGraph:
    """
    A builder of Graphviz inheritance graphs.

    Here we build the inheritance graph of all classes found in
    :py:mod:`uqbar.containers`:

    ::

        >>> import uqbar.apis
        >>> graph = uqbar.apis.InheritanceGraph(
        ...     package_paths=['uqbar.containers'],
        ...     )
        >>> print(graph)
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
                "uqbar.containers.DependencyGraph.DependencyGraph" [label="Dependency\\nGraph"];
                "uqbar.containers.UniqueTreeContainer.UniqueTreeContainer" [label="Unique\\nTree\\nContainer"];
                "uqbar.containers.UniqueTreeNode.UniqueTreeNode" [label="Unique\\nTree\\nNode"];
                "uqbar.containers.UniqueTreeNode.UniqueTreeNode" -> "uqbar.containers.UniqueTreeContainer.UniqueTreeContainer";
            }
            "builtins.object" -> "uqbar.containers.DependencyGraph.DependencyGraph";
            "builtins.object" -> "uqbar.containers.UniqueTreeNode.UniqueTreeNode";
        }


    We can calculate the "aspect ratio" of the graph - the number of
    generations vs the maximum generation size. This can be a useful metric for
    applying additional post-processing like Graphviz' ``unflatten`` utility:

    ::

        >>> graph.aspect_ratio
        (2, 2)

    Lineage paths constrain the classes in the graph to only those whose
    antecedents or descendants pass through the classes identified by those
    lineage paths. Here we collect all classes defined in :py:mod:`uqbar` and
    then constrain to those passing through :py:mod:`uqbar.containers`:

    ::

        >>> graph = uqbar.apis.InheritanceGraph(
        ...     package_paths=['uqbar'],
        ...     lineage_paths=['uqbar.containers'],
        ...     )
        >>> print(graph)
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
                "uqbar.apis.ModuleNode.ModuleNode" [label="Module\\nNode"];
                "uqbar.apis.PackageNode.PackageNode" [label="Package\\nNode"];
            }
            subgraph "cluster_uqbar.containers" {
                graph [label="uqbar.containers"];
                node [color=3];
                "uqbar.containers.DependencyGraph.DependencyGraph" [color=black,
                    fontcolor=white,
                    label="Dependency\\nGraph"];
                "uqbar.containers.UniqueTreeContainer.UniqueTreeContainer" [color=black,
                    fontcolor=white,
                    label="Unique\\nTree\\nContainer"];
                "uqbar.containers.UniqueTreeNode.UniqueTreeNode" [color=black,
                    fontcolor=white,
                    label="Unique\\nTree\\nNode"];
                "uqbar.containers.UniqueTreeNode.UniqueTreeNode" -> "uqbar.containers.UniqueTreeContainer.UniqueTreeContainer";
            }
            subgraph "cluster_uqbar.graphs" {
                graph [label="uqbar.graphs"];
                node [color=4];
                "uqbar.graphs.Attachable.Attachable" [label=Attachable];
                "uqbar.graphs.Graph.Graph" [label="Graph"];
                "uqbar.graphs.HRule.HRule" [label=HRule];
                "uqbar.graphs.LineBreak.LineBreak" [label="Line\\nBreak"];
                "uqbar.graphs.Node.Node" [label="Node"];
                "uqbar.graphs.RecordField.RecordField" [label="Record\\nField"];
                "uqbar.graphs.RecordGroup.RecordGroup" [label="Record\\nGroup"];
                "uqbar.graphs.Table.Table" [label=Table];
                "uqbar.graphs.TableCell.TableCell" [label="Table\\nCell"];
                "uqbar.graphs.TableRow.TableRow" [label="Table\\nRow"];
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

    ::

        >>> graph.aspect_ratio
        (3, 8)

    :param package_paths: a sequence of package path strings, classes or
        modules to seed the inheritance graph with

    :param lineage_paths: a sequence of package path strings, classes or
        modules to constrain the inheritance graph with

    """

    ### INITIALIZER ###

    def __init__(
        self,
        package_paths: Sequence[Union[str, type, types.ModuleType]],
        lineage_paths: Sequence[Union[str, type, types.ModuleType]]=None,
    ) -> None:
        self._package_paths = self._initialize_package_paths(package_paths)
        self._lineage_paths = self._initialize_package_paths(
            lineage_paths or [])
        initial_classes = self._collect_classes(
            self._package_paths,
        )
        self._lineage_classes = self._collect_classes(
            self._lineage_paths,
            recurse_subpackages=False,
        )
        (
            self._parents_to_children,
            self._children_to_parents,
            ) = self._build_mappings(initial_classes)
        if self._lineage_paths:
            self._strip_nonlineage_classes()
        parent_classes = set(self._parents_to_children)
        child_classes = set(self._children_to_parents)
        self._classes = parent_classes.union(child_classes)
        self._aspect_ratio = self._calculate_aspect_ratio()

    ### SPECIAL METHODS ###

    def __len__(self) -> int:
        return len(set(self._parents_to_children).union(
            set(self._children_to_parents)))

    def __str__(self) -> str:
        graph = self.build_graph()
        return format(graph, 'graphviz')

    ### PUBLIC METHODS ###

    def build_graph(self, urls=None):
        urls = urls or {}
        graph = uqbar.graphs.Graph(
            name='InheritanceGraph',
            attributes={
                'bgcolor': 'transparent',
                'color': 'lightsteelblue2',
                'fontname': 'Arial',
                'fontsize': 10,
                'outputorder': 'edgesfirst',
                'overlap': 'prism',
                'penwidth': 2,
                'rankdir': 'LR',
                'splines': 'spline',
                'style': ['dashed', 'rounded'],
                'truecolor': True,
                },
            edge_attributes={
                'color': 'lightslategrey',
                'penwidth': 1,
                },
            node_attributes={
                'colorscheme': 'pastel19',
                'fontname': 'Arial',
                'fontsize': 10,
                'width': 0,
                'height': 0,
                'penwidth': 2,
                'shape': 'box',
                'style': ['filled', 'rounded'],
                },
            )
        classes_to_nodes: Dict[type, uqbar.graphs.Node] = {}
        for class_ in sorted(
            self._classes,
            key=lambda x: (x.__module__, x.__name__),
        ):
            node = self._get_or_create_node(class_, graph, urls)
            classes_to_nodes[class_] = node

        for parent_class, child_classes in self._parents_to_children.items():
            parent_node = classes_to_nodes[parent_class]
            for child_class in sorted(
                child_classes,
                key=lambda x: (x.__module__, x.__name__),
            ):
                child_node = classes_to_nodes[child_class]
                parent_node.attach(child_node)
        for i, cluster in enumerate(sorted(graph[:], key=lambda x: x.name)):
            cluster.node_attributes['color'] = i % 9 + 1
        return graph

    ### PRIVATE METHODS ###

    def _calculate_aspect_ratio(self):
        def calculate_depth(class_, depth=0):
            parents = self._children_to_parents.get(class_, ())
            while parents:
                depth += 1
                new_parents = set()
                for parent in parents:
                    new_parents.update(
                        self._children_to_parents.get(parent, ()))
                parents = new_parents
            return depth

        if not self._children_to_parents:
            return None

        class_to_depth = {}
        for class_ in self._children_to_parents:
            class_to_depth[class_] = calculate_depth(class_)
        depth_to_classes = {}
        for class_, depth in class_to_depth.items():
            depth_to_classes.setdefault(depth, set()).add(class_)
        width = len(depth_to_classes)
        height = max(len(classes) for classes in depth_to_classes.values())
        return width, height

    def _get_or_create_cluster(self, class_, graph):
        cluster_name = class_.__module__
        if cluster_name.rpartition('.')[-1] == class_.__name__:
            cluster_name, _, _ = cluster_name.rpartition('.')
        if cluster_name in graph:
            cluster = graph[cluster_name]
        else:
            attributes = dict(label=cluster_name)
            cluster = uqbar.graphs.Graph(
                name=cluster_name,
                is_cluster=True,
                attributes=attributes,
                )
            graph.append(cluster)
        return cluster

    def _get_or_create_node(self, class_, graph, urls):
        url_name = class_.__name__
        if class_.__module__ not in ('__builtins__', 'builtins'):
            url_name = class_.__module__ + '.' + url_name
        node_name = '{}.{}'.format(class_.__module__, class_.__name__)
        if node_name in graph:
            node = graph[node_name]
        else:
            cluster = self._get_or_create_cluster(class_, graph)
            label = r'\n'.join(uqbar.strings.delimit_words(class_.__name__))
            attributes = dict(label=label)
            if url_name in urls:
                attributes['URL'] = urls[url_name]
                attributes['target'] = '_top'
            if inspect.isabstract(class_):
                attributes['shape'] = 'oval'
                attributes['style'] = ['bold']
            if class_ in self._lineage_classes:
                attributes['color'] = 'black'
                attributes['fontcolor'] = 'white'
                if inspect.isabstract(class_):
                    attributes['style'] = ['bold', 'filled']
            node = uqbar.graphs.Node(
                name=node_name,
                attributes=attributes,
                )
            cluster.append(node)
        return node

    def _build_mappings(
        self,
        classes: Sequence[type],
        ) -> Tuple[
            Mapping[type, Sequence[type]],
            Mapping[type, Sequence[type]],
            ]:
        """
        Collect all bases and organize into parent/child mappings.
        """
        parents_to_children: MutableMapping[type, Set[type]] = {}
        children_to_parents: MutableMapping[type, Set[type]] = {}
        visited_classes: Set[type] = set()
        class_stack = list(classes)
        while class_stack:
            class_ = class_stack.pop()
            if class_ in visited_classes:
                continue
            visited_classes.add(class_)
            for base in class_.__bases__:
                if base not in visited_classes:
                    class_stack.append(base)
                parents_to_children.setdefault(base, set()).add(class_)
                children_to_parents.setdefault(class_, set()).add(base)
        sorted_parents_to_children: MutableMapping[type, List[type]] = \
            collections.OrderedDict()
        for parent, children in sorted(
            parents_to_children.items(),
            key=lambda x: (x[0].__module__, x[0].__name__)
        ):
            sorted_parents_to_children[parent] = sorted(
                children, key=lambda x: (x.__module__, x.__name__))
        sorted_children_to_parents: MutableMapping[type, List[type]] = \
            collections.OrderedDict()
        for child, parents in sorted(
            children_to_parents.items(),
            key=lambda x: (x[0].__module__, x[0].__name__)
        ):
            sorted_children_to_parents[child] = sorted(
                parents, key=lambda x: (x.__module__, x.__name__))
        return sorted_parents_to_children, sorted_children_to_parents

    def _collect_classes(
        self,
        package_paths: Sequence[str],
        recurse_subpackages: bool=True,
    ) -> Sequence[type]:
        """
        Collect all classes defined in/under ``package_paths``.
        """
        import uqbar.apis
        classes = []
        initial_source_paths: Set[str] = set()
        # Graph source paths and classes
        for path in package_paths:
            try:
                module = importlib.import_module(path)
                if hasattr(module, '__path__'):
                    initial_source_paths.update(getattr(module, '__path__'))
                else:
                    initial_source_paths.add(module.__file__)
            except ModuleNotFoundError:
                path, _, class_name = path.rpartition('.')
                module = importlib.import_module(path)
                classes.append(getattr(module, class_name))
        # Iterate source paths
        for source_path in uqbar.apis.collect_source_paths(
            initial_source_paths,
            recurse_subpackages=recurse_subpackages,
        ):
            package_path = uqbar.apis.source_path_to_package_path(
                source_path)
            module = importlib.import_module(package_path)
            # Grab any defined classes
            for name in dir(module):
                if name.startswith('_'):
                    continue
                object_ = getattr(module, name)
                if (
                    isinstance(object_, type) and
                    object_.__module__ == module.__name__
                ):
                    classes.append(object_)
        return sorted(classes, key=lambda x: (x.__module__, x.__name__))

    def _initialize_package_paths(
        self,
        package_paths: Sequence[Any],
    ) -> Sequence[str]:
        result = []
        for path in package_paths:
            if isinstance(path, type):
                result.append('{}.{}'.format(path.__module__, path.__name__))
            elif isinstance(path, types.ModuleType):
                result.append(path.__name__)
            elif not isinstance(path, str):
                path = type(path)
                result.append('{}.{}'.format(path.__module__, path.__name__))
            else:
                result.append(path)
        return tuple(sorted(result))

    def _strip_nonlineage_classes(self):
        def _recurse_upward(current_class):
            visited_classes.add(current_class)
            for parent in self._children_to_parents.get(current_class, ()):
                _recurse_upward(parent)

        def _recurse_downward(current_class):
            visited_classes.add(current_class)
            for child in self._parents_to_children.get(current_class, ()):
                _recurse_downward(child)

        visited_classes = set()
        # Check for hierarchies interecting the lineage classes
        for class_ in self._lineage_classes:
            _recurse_upward(class_)
            _recurse_downward(class_)
        # Check if lineage paths are prefixes for class module paths
        lineage_paths_parts = [
            lineage_path.split('.')
            for lineage_path in self._lineage_paths
            ]
        for class_ in self._children_to_parents:
            module_parts = class_.__module__.split('.')
            for parts in lineage_paths_parts:
                if module_parts[:len(parts)] == parts:
                    _recurse_upward(class_)
                    _recurse_downward(class_)
                    break

        for parent, children in tuple(self._parents_to_children.items()):
            if parent in visited_classes:
                continue
            for child in children:
                self._children_to_parents.get(child, []).remove(parent)
            self._parents_to_children.pop(parent)

        for child, parents in tuple(self._children_to_parents.items()):
            if child in visited_classes:
                continue
            for parent in parents:
                self._parents_to_children.get(parent, []).remove(child)
            self._children_to_parents.pop(child)

    ### PUBLIC PROPERTIES ###

    @property
    def aspect_ratio(self):
        return self._aspect_ratio

    @property
    def children_to_parents(self):
        return self._children_to_parents

    @property
    def classes(self):
        return self._classes

    @property
    def parents_to_children(self):
        return self._parents_to_children
