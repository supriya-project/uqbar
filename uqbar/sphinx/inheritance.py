"""
Uqbar Sphinx inheritance graph extension.

Install by adding ``'uqbar.sphinx.inheritance'`` to the ``extensions`` list in
your Sphinx configuration.

Invoke by adding the following directive to your ReST source:

::

    .. inheritance-graph:: some.python.path

This will generate Graphviz output mediated by a
:py:class:`uqbar.apis.InheritanceGraph` instance. You can specify lineage paths
by adding a ``:lineage:`` option to the directive:

::

    .. inheritance-graph:: some.python.path
       :lineage: some.lineage.path

Both the main argument to the directive and the lineage option can take
multiple paths, separated by spaces:

::

    .. inheritance-graph:: path.one path.two
       :lineage: path.three path.four path.five

"""
import os
import pathlib
import uqbar.apis
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.ext.graphviz import render_dot_html, render_dot_latex
from typing import List, Mapping


class inheritance_diagram(nodes.General, nodes.Element):
    """
    A docutils node to use as a placeholder for the inheritance diagram.
    """
    pass


class InheritanceDiagram(Directive):
    """
    Run when the inheritance_diagram directive is first encountered.
    """
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {'lineage': directives.unchanged}

    def run(self) -> List[nodes.Node]:
        node = inheritance_diagram()
        node.document = self.state.document
        package_paths = self.arguments[0].split()
        lineage_paths = self.options.get('lineage', '').split() or None
        # Create the graph
        try:
            graph = uqbar.apis.InheritanceGraph(
                package_paths=package_paths,
                lineage_paths=lineage_paths,
                )
        except Exception as error:
            warning = node.document.reporter.warning(
                error.args[0],
                line=self.lineno,
                )
            return [warning]
        if not graph.classes:
            return []
        # Create xref nodes for each target of the graph's image map and add
        # them to the doc tree so that Sphinx can resolve the references to
        # real URLs later.  These nodes will eventually be removed from the
        # doctree after we're done with them.
        env = self.state.document.settings.env
        class_role = env.get_domain('py').role('class')
        for class_ in graph.classes:
            url_name = class_.__name__
            if class_.__module__ not in ('__builtins__', 'builtins'):
                url_name = class_.__module__ + '.' + url_name
            refnodes, _ = class_role(
                'class', ':class:`{}`'.format(url_name),
                url_name, 0, self.state,
                )
            node.extend(refnodes)
        # Store the graph object so we can use it to generate the dot file
        # later on
        node['graph'] = graph
        return [node]


def build_urls(
    self: nodes.NodeVisitor,
    node: inheritance_diagram,
    ) -> Mapping[str, str]:
    current_filename = self.builder.current_docname + self.builder.out_suffix
    urls = {}
    for child in node:
        # Another document
        if child.get('refuri') is not None:
            uri = child.get('refuri')
            package_path = child['reftitle']
            if uri.startswith('http'):
                _, _, package_path = uri.partition('#')
            else:
                uri = (
                    pathlib.Path('..') /
                    pathlib.Path(current_filename).parent /
                    pathlib.Path(uri)
                    )
                uri = str(uri).replace(os.path.sep, '/')
            urls[package_path] = uri
        # Same document
        elif child.get('refid') is not None:
            urls[child['reftitle']] = '../' + current_filename + '#' + child.get('refid')
    return urls


def html_visit_inheritance_diagram(
    self: nodes.NodeVisitor,
    node: inheritance_diagram,
    ) -> None:
    graph = node['graph']
    urls = build_urls(self, node)
    dot_code = format(graph.build_graph(urls), 'graphviz')
    render_dot_html(self, node, dot_code, {}, 'inheritance', 'inheritance')
    raise nodes.SkipNode


def latex_visit_inheritance_diagram(
    self: nodes.NodeVisitor,
    node: inheritance_diagram,
    ) -> None:
    graph = node['graph']
    dot_code = graph.build_graph()
    render_dot_latex(self, node, dot_code, {}, 'inheritance', 'inheritance')
    raise nodes.SkipNode


def skip(self: nodes.NodeVisitor, node: inheritance_diagram) -> None:
    raise nodes.SkipNode


def setup(app):
    app.setup_extension('sphinx.ext.graphviz')
    app.add_node(
        inheritance_diagram,
        html=(html_visit_inheritance_diagram, None),
        latex=(latex_visit_inheritance_diagram, None),
        man=(skip, None),
        texinfo=(skip, None),
        text=(skip, None),
        )
    app.add_directive('inheritance-diagram', InheritanceDiagram)
