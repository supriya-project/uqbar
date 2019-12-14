import abc
import copy
import hashlib
import json
import pathlib
import subprocess

from docutils.nodes import FixedTextElement, General, SkipNode

from uqbar.graphs import Grapher
from uqbar.strings import normalize

from .console import Console
from .sphinx import UqbarBookDirective


class Extension:
    @classmethod
    @abc.abstractmethod
    def setup_console(cls, console: Console, monkeypatch):
        """
        Perform console setup tasks before executing a suite of code blocks,
        e.g. monkeypatching IO operations to allow media capture.
        """
        raise NotImplementedError

    @classmethod
    def setup_proxy_key(cls, key):
        UqbarBookDirective.option_spec[key] = lambda x: json.loads(x or "{}")

    @classmethod
    @abc.abstractmethod
    def setup_sphinx(cls, app):
        """
        Setup Sphinx, e.g. register custom nodes and visitors.
        """
        raise NotImplementedError

    @classmethod
    def teardown_console(cls, app):
        """
        Perform console teardown tasks.
        """
        pass

    @staticmethod
    def visit_block_html(self, node):
        raise SkipNode

    @staticmethod
    def visit_block_latex(self, node):
        raise SkipNode

    @staticmethod
    def depart_block_text(self, node):
        self.end_state(wrap=False)

    @staticmethod
    def visit_block_text(self, node):
        self.new_state()


class GraphExtension(Extension):
    template = normalize(
        """
        <a href="{dot_file_path}" title="{title}" class="{css_class}">
            <img src="{image_file_path}" alt="{alt}"/>
        </a>
        """
    )

    class graphviz_block(General, FixedTextElement):
        pass

    @classmethod
    def setup_console(cls, console, monkeypatch):
        monkeypatch.setattr(
            Grapher,
            "__call__",
            lambda self: console.push_proxy(
                cls(
                    self.graphable,
                    self.layout,
                    **console.proxy_options.get("graphviz", {}),
                ),
            ),
        )

    @classmethod
    def setup_sphinx(cls, app):
        app.add_node(
            cls.graphviz_block,
            html=[cls.visit_block_html, None],
            latex=[cls.visit_block_latex, None],
            text=[cls.visit_block_text, cls.depart_block_text],
        )
        cls.setup_proxy_key("graphviz")

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
        sha256 = hashlib.sha256()
        sha256.update(node[0].encode())
        sha256.update(node["layout"].encode())
        hexdigest = sha256.hexdigest()
        base_path = output_path / "graphviz-{}".format(hexdigest)
        base_path.parent.mkdir(exist_ok=True, parents=True)
        image_file_path = base_path.with_suffix(suffix)
        dot_file_path = base_path.with_suffix(".dot")
        if image_file_path.exists() and dot_file_path.exists():
            return image_file_path
        if not dot_file_path.exists():
            dot_file_path.write_text(node[0])
        if not image_file_path.exists():
            command = "{layout} -T {format} -o {image_path} {dot_path}".format(
                layout=node["layout"],
                format=suffix.strip("."),
                image_path=image_file_path,
                dot_path=dot_file_path,
            )
            subprocess.call(command, shell=True)
            if suffix == ".svg":
                cls.clean_svg(image_file_path)
        return image_file_path

    @staticmethod
    def visit_block_html(self, node):
        absolute_image_file_path = GraphExtension.render_image(
            node, pathlib.Path(self.builder.outdir) / "_images", ".svg"
        )
        relative_image_file_path = (
            pathlib.Path(self.builder.imgpath) / absolute_image_file_path.name
        )
        result = GraphExtension.template.format(
            dot_file_path=relative_image_file_path.with_suffix(".dot"),
            image_file_path=relative_image_file_path,
            title="",
            alt="",
            css_class="",
        )
        self.body.append(result)
        raise SkipNode
