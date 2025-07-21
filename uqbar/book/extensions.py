import copy
import hashlib
import pathlib
import subprocess

from docutils.nodes import FixedTextElement, General, SkipNode

from ..graphs import Grapher
from . import Extension


class GraphExtension(Extension):
    template = (
        '<div class="uqbar-book">'
        '<a href="{dot_file_path}" title="{title}">'
        '<img src="{image_file_path}" alt="{alt}"/>'
        "</a>"
        "</div>"
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
                    **{
                        key.replace("graphviz/", "").replace("-", "_"): value
                        for key, value in console.proxy_options.items()
                        if key.startswith("graphviz/")
                    },
                )
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
        )
        self.body.append(result)
        raise SkipNode
