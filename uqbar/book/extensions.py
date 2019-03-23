import abc
import copy
import hashlib
import pathlib
import subprocess

from docutils.nodes import FixedTextElement, General, SkipNode

import uqbar.book.console
from uqbar.graphs import Grapher
from uqbar.strings import normalize


class Extension:
    @abc.abstractmethod
    def setup(self, console: "uqbar.book.console.Console", monkeypatch):
        raise NotImplementedError

    def teardown(self):
        pass


class GrapherExtension(Extension):
    def setup(self, console, monkeypatch):
        monkeypatch.setattr(
            Grapher,
            "__call__",
            lambda self: console.push_proxy(
                GraphableProxy(self.graphable, self.layout)
            ),
        )

    @classmethod
    def setup_sphinx(cls, app):
        GraphableProxy.setup_sphinx(app)


class GraphableProxy:

    template = normalize(
        """
        <a href="{dot_file_path}" title="{title}" class="{cls}">
            <img src="{image_file_path}" alt="{alt}"/>
        </a>
        """
    )

    class graphviz_block(General, FixedTextElement):
        pass

    def __init__(self, graphable, layout):
        try:
            self.graphable = copy.deepcopy(graphable)
        except Exception:
            self.graphable = copy.deepcopy(graphable.__graph__())
        self.layout = layout

    def to_docutils(self):
        try:
            graphviz_graph = self.graphable.__graph__()
            code = format(graphviz_graph, "graphviz")
        except AttributeError:
            code = self.graphable.__format_graphviz__()
        node = self.graphviz_block(code, code)
        node["layout"] = self.layout
        return [node]

    @classmethod
    def clean_svg(cls, svg_path):
        pass

    @classmethod
    def render_image(cls, node, output_path, suffix):
        image_path = output_path / "_images"
        sha256 = hashlib.sha256()
        sha256.update(node[0].encode())
        sha256.update(node["layout"].encode())
        hexdigest = sha256.hexdigest()
        base_path = image_path / "graphviz-{}".format(hexdigest)
        base_path.parent.mkdir(exist_ok=True, parents=True)
        image_file_path = base_path.with_suffix(suffix)
        dot_file_path = base_path.with_suffix(".dot")
        if image_file_path.exists() and dot_file_path.exists():
            return image_file_path
        if not dot_file_path.exists():
            dot_file_path.write_text(node[0])
        if not image_file_path.exists():
            command = "{layout} -T {format} -o {output_path} {input_path}".format(
                layout=node["layout"],
                format=suffix.strip("."),
                output_path=image_file_path,
                input_path=dot_file_path,
            )
            subprocess.call(command, shell=True)
            if suffix == ".svg":
                cls.clean_svg(image_file_path)
        return image_file_path

    @classmethod
    def setup_sphinx(cls, app):
        app.add_node(
            cls.graphviz_block,
            html=[cls.visit_graphviz_block_html, None],
            latex=[cls.visit_graphviz_block_latex, None],
            text=[cls.visit_graphviz_block_text, cls.depart_graphviz_block_text],
        )

    @staticmethod
    def visit_graphviz_block_html(self, node):
        absolute_image_file_path = GraphableProxy.render_image(
            node, pathlib.Path(self.builder.outdir), ".svg"
        )
        relative_image_file_path = (
            pathlib.Path(self.builder.imgpath) / absolute_image_file_path.name
        )
        template = normalize(
            """
            <a href="{dot_file_path}" title="{title}" class="{css_class}">
                <img src="{image_file_path}" alt="{alt}"/>
            </a>
            """
        )
        result = template.format(
            dot_file_path=relative_image_file_path.with_suffix(".dot"),
            image_file_path=relative_image_file_path,
            title="",
            alt="",
            css_class="",
        )
        self.body.append(result)
        raise SkipNode

    @staticmethod
    def visit_graphviz_block_latex(self, node):
        raise SkipNode

    @staticmethod
    def depart_graphviz_block_text(self, node):
        self.end_state(wrap=False)

    @staticmethod
    def visit_graphviz_block_text(self, node):
        self.new_state()
