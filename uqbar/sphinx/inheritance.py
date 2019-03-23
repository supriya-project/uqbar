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
import math
import os
import pathlib
import subprocess
from typing import Any, Dict, List, Mapping

from docutils.nodes import Element  # type: ignore
from docutils.nodes import General, Node, NodeVisitor, SkipNode
from docutils.parsers.rst import Directive, directives  # type: ignore
from sphinx.ext.graphviz import render_dot_html  # type: ignore
from sphinx.ext.graphviz import render_dot_latex

import uqbar.apis


class inheritance_diagram(General, Element):
    """
    A docutils node to use as a placeholder for the inheritance diagram.
    """

    __documentation_ignore_inherited__ = True


class InheritanceDiagram(Directive):
    """
    Runs when the inheritance_diagram directive is first encountered.
    """

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {"lineage": directives.unchanged}

    __documentation_ignore_inherited__ = True

    def run(self) -> List[Node]:
        node = inheritance_diagram()
        node.document = self.state.document
        package_paths = self.arguments[0].split()
        lineage_paths = self.options.get("lineage", "").split() or None
        # Create the graph
        try:
            graph = uqbar.apis.InheritanceGraph(
                package_paths=package_paths, lineage_paths=lineage_paths
            )
        except Exception as error:
            warning = node.document.reporter.warning(error.args[0], line=self.lineno)
            return [warning]
        if not graph.all_class_paths:
            return []
        # Create xref nodes for each target of the graph's image map and add
        # them to the doc tree so that Sphinx can resolve the references to
        # real URLs later.  These nodes will eventually be removed from the
        # doctree after we're done with them.
        env = self.state.document.settings.env
        class_role = env.get_domain("py").role("class")
        for class_path in graph.all_class_paths:
            module_name, _, class_name = class_path.rpartition(".")
            url_name = class_name
            if module_name not in ("__builtins__", "builtins"):
                url_name = class_path
            refnodes, _ = class_role(
                "class", ":class:`{}`".format(url_name), url_name, 0, self.state
            )
            node.extend(refnodes)
        # Store the graph object so we can use it to generate the dot file
        # later on
        node["graph"] = graph
        return [node]


def build_urls(self: NodeVisitor, node: inheritance_diagram) -> Mapping[str, str]:
    """
    Builds a mapping of class paths to URLs.
    """
    current_filename = self.builder.current_docname + self.builder.out_suffix
    urls = {}
    for child in node:
        # Another document
        if child.get("refuri") is not None:
            uri = child.get("refuri")
            package_path = child["reftitle"]
            if uri.startswith("http"):
                _, _, package_path = uri.partition("#")
            else:
                uri = (
                    pathlib.Path("..")
                    / pathlib.Path(current_filename).parent
                    / pathlib.Path(uri)
                )
                uri = str(uri).replace(os.path.sep, "/")
            urls[package_path] = uri
        # Same document
        elif child.get("refid") is not None:
            urls[child["reftitle"]] = (
                "../" + current_filename + "#" + child.get("refid")
            )
    return urls


def html_visit_inheritance_diagram(
    self: NodeVisitor, node: inheritance_diagram
) -> None:
    """
    Builds HTML output from an :py:class:`~uqbar.sphinx.inheritance.inheritance_diagram` node.
    """
    inheritance_graph = node["graph"]
    urls = build_urls(self, node)
    graphviz_graph = inheritance_graph.build_graph(urls)
    dot_code = format(graphviz_graph, "graphviz")
    # TODO: We can perform unflattening here
    aspect_ratio = inheritance_graph.aspect_ratio
    if aspect_ratio:
        aspect_ratio = math.ceil(math.sqrt(aspect_ratio[1] / aspect_ratio[0]))
    if aspect_ratio > 1:
        process = subprocess.Popen(
            ["unflatten", "-l", str(aspect_ratio), "-c", str(aspect_ratio), "-f"],
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate(dot_code.encode())
        dot_code = stdout.decode()
    render_dot_html(self, node, dot_code, {}, "inheritance", "inheritance")
    raise SkipNode


def latex_visit_inheritance_diagram(
    self: NodeVisitor, node: inheritance_diagram
) -> None:
    """
    Builds LaTeX output from an :py:class:`~uqbar.sphinx.inheritance.inheritance_diagram` node.
    """
    inheritance_graph = node["graph"]
    graphviz_graph = inheritance_graph.build_graph()
    graphviz_graph.attributes["size"] = 6.0
    dot_code = format(graphviz_graph, "graphviz")
    render_dot_latex(self, node, dot_code, {}, "inheritance")
    raise SkipNode


def skip(self: NodeVisitor, node: inheritance_diagram) -> None:
    """
    Skip generating output, for non-supported builders.
    """
    raise SkipNode


def setup(app) -> Dict[str, Any]:
    """
    Sets up Sphinx extension.
    """
    app.setup_extension("sphinx.ext.graphviz")
    app.add_node(
        inheritance_diagram,
        html=(html_visit_inheritance_diagram, None),
        latex=(latex_visit_inheritance_diagram, None),
        man=(skip, None),
        texinfo=(skip, None),
        text=(skip, None),
    )
    app.add_directive("inheritance-diagram", InheritanceDiagram)
    return {
        "version": uqbar.__version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
