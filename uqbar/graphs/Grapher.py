import datetime
import hashlib
import pathlib
import re
import subprocess
import sys
import tempfile
from typing import Generator, Sequence, Tuple

from uqbar.io import Timer


class Grapher:

    ### CLASS VARIABLES ###

    _valid_formats = ("png", "pdf", "svg")
    _valid_layouts = ("circo", "dot", "fdp", "neato", "osage", "sfdp", "twopi")

    ### INITIALIZER ###

    def __init__(
        self, graphable, format_="pdf", layout="dot", output_directory=None,
    ):
        if layout not in self._valid_layouts:
            raise ValueError("Invalid layout: {layout!r}")
        if format_ not in self._valid_formats:
            raise ValueError("Invalid format: {format_!r}")
        self.graphable = graphable
        self.format_ = format_
        self.layout = layout
        self.output_directory = pathlib.Path(output_directory or ".")

    ### SPECIAL METHODS ###

    def __call__(self):
        with Timer() as format_timer:
            string = self.get_string()
        format_time = format_timer.elapsed_time
        layout = self.get_layout()
        format_ = self.get_format()
        render_prefix = self.get_render_prefix(string)
        render_directory_path = self.get_render_directory()
        input_path = (render_directory_path / render_prefix).with_suffix(".dot")
        self.persist_string(string, input_path)
        render_command = self.get_render_command(format_, input_path, layout)
        with Timer() as render_timer:
            log, success = self.run_command(render_command)
        render_time = render_timer.elapsed_time
        self.persist_log(log, input_path.with_suffix(".log"))
        output_directory_path = self.get_output_directory()
        output_paths = self.migrate_assets(
            render_prefix, render_directory_path, output_directory_path
        )
        openable_paths = []
        for output_path in self.get_openable_paths(format_, output_paths):
            openable_paths.append(output_path)
            self.open_output_path(output_path)
        return output_path, format_time, render_time, success, log

    ### PUBLIC METHODS ###

    def get_format(self) -> str:
        return self.format_

    def get_layout(self) -> str:
        return self.layout

    def get_openable_paths(
        self, format_, output_paths
    ) -> Generator[pathlib.Path, None, None]:
        for path in output_paths:
            if path.suffix == f".{format_}":
                yield path

    def get_output_directory(self) -> pathlib.Path:
        return self.output_directory

    def get_render_command(self, format_, input_path, layout) -> str:
        parts = [
            layout,
            "-v",
            "-T",
            format_,
            "-o",
            str(input_path.with_suffix("." + format_)),
            str(input_path),
        ]
        return " ".join(parts)

    def get_render_directory(self):
        return pathlib.Path(tempfile.mkdtemp())

    def get_render_prefix(self, string) -> str:
        timestamp = re.sub(r"[^\w]", "-", datetime.datetime.now().isoformat())
        checksum = hashlib.sha1(string.encode()).hexdigest()[:7]
        return f"{timestamp}-{checksum}"

    def get_string(self) -> str:
        try:
            graphviz_graph = self.graphable.__graph__()
            return format(graphviz_graph, "graphviz")
        except AttributeError:
            return self.graphable.__format_graphviz__()

    def migrate_assets(
        self, render_prefix, render_directory, output_directory
    ) -> Sequence[pathlib.Path]:
        migrated_assets = []
        for old_path in render_directory.iterdir():
            if not old_path.name.startswith(render_prefix):
                continue
            new_path = output_directory / old_path.name
            old_path.rename(new_path)
            migrated_assets.append(new_path)
        return migrated_assets

    def open_output_path(self, output_path):
        viewer = "open"
        if sys.platform.lower().startswith("linux"):
            viewer = "xdg-open"
        subprocess.run(f"{viewer} {output_path}", shell=True, check=True)

    def persist_log(self, string, input_path):
        input_path.write_text(string)

    def persist_string(self, string, input_path):
        input_path.write_text(string)

    def run_command(self, command: str) -> Tuple[str, int]:
        completed_process = subprocess.run(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        return completed_process.stdout.decode(), completed_process.returncode == 0
