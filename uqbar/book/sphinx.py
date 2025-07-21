import contextlib
import importlib
import inspect
import itertools
import logging
import pickle
import sqlite3
import traceback
from pathlib import Path
from typing import Any, Dict, Generator

from docutils.frontend import get_default_settings
from docutils.nodes import Element, General, doctest_block, document, literal_block
from docutils.parsers.rst import Directive, Parser
from docutils.parsers.rst.directives import flag
from docutils.utils import new_document
from sphinx.addnodes import desc_signature
from sphinx.util.nodes import set_source_info
from typing_extensions import ClassVar

from .console import Console, ConsoleError, ConsoleInput, ConsoleOutput
from .extensions import Extension

logger = logging.getLogger(__name__)

try:
    import black

    def black_format(lines: list[str]) -> list[str]:
        mode = black.FileMode(
            line_length=80, target_versions=set([black.TargetVersion.PY310])
        )
        return black.format_str("\n".join(lines), mode=mode).splitlines()

except ImportError:

    def black_format(lines: list[str]) -> list[str]:
        return lines


class uqbar_book_defaults_block(General, Element):
    __documentation_ignore_inherited__ = True


class uqbar_book_import_block(General, Element):
    __documentation_ignore_inherited__ = True


class UqbarBookDirective(Directive):
    __documentation_ignore_inherited__ = True

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec: ClassVar[Dict[str, Any]] = {"allow-exceptions": flag, "hide": flag}

    def run(self) -> list[literal_block]:
        self.assert_has_content()
        code = "\n".join(self.content)
        block = literal_block(code, code)
        block.line = self.content_offset  # set the content line number
        set_source_info(self, block)
        for key, spec in self.option_spec.items():
            if key not in self.options:
                continue
            option = self.options[key]
            if spec == flag:
                option = True
            block[key] = option
        return [block]


class UqbarBookDefaultsDirective(Directive):
    __documentation_ignore_inherited__ = True

    has_content = False
    required_arguments = 0
    optional_arguments = 0
    option_spec: ClassVar[Dict[str, Any]] = {}

    def run(self) -> list[uqbar_book_defaults_block]:
        block = uqbar_book_defaults_block()
        for key, value in self.options.items():
            block[key] = value
        return [block]


class UqbarBookImportDirective(Directive):
    __documentation_ignore_inherited__ = True

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    option_spec = {"hide": flag}

    def run(self) -> list[uqbar_book_import_block]:
        block = uqbar_book_import_block()
        block["path"] = self.arguments[0]
        block.line = self.content_offset  # set the content line number
        set_source_info(self, block)
        if "hide" in self.options:
            block["hide"] = True
        return [block]


def collect_literal_blocks(document):
    prototype = (
        literal_block,
        doctest_block,
        uqbar_book_defaults_block,
        uqbar_book_import_block,
    )
    blocks = []
    for block in document.findall(lambda node: isinstance(node, prototype)):
        if not isinstance(block, (uqbar_book_defaults_block, uqbar_book_import_block)):
            contents = block[0]
            if isinstance(contents, literal_block):
                contents = contents[0]
            if not contents.strip().startswith(">>>"):
                continue
        blocks.append(block)
    return blocks


def create_cache_db(path: Path | str) -> sqlite3.Connection:
    connection = sqlite3.connect(str(path))
    connection.execute("CREATE TABLE cache (path TEXT, data BLOB, hits NUMBER);")
    connection.commit()
    return connection


def query_cache_db(connection: sqlite3.Connection, cache_path: str):
    result = None
    for row in connection.execute(
        "SELECT data, hits FROM cache WHERE path = ?", (cache_path,)
    ):
        result, hits = row
    if not result:
        return None
    connection.execute(
        "UPDATE cache SET hits = ? WHERE path = ?", (hits + 1, cache_path)
    )
    connection.commit()
    return pickle.loads(result)


def update_cache_db(connection: sqlite3.Connection, cache_path: str, data):
    connection.execute(
        "INSERT INTO cache VALUES (?, ?, 0)", (cache_path, pickle.dumps(data))
    )
    connection.commit()


def group_literal_blocks_by_cache_path(blocks):
    cache_mapping = {None: [[]]}
    last_cache_path = None
    for block in blocks:
        cache_path = literal_block_to_cache_path(block)
        if cache_path is None:
            cache_mapping[None][0].append(block)
            last_cache_path = None
        else:
            if cache_path != last_cache_path:
                block_list = []
                cache_mapping.setdefault(cache_path, []).append(block_list)
            cache_mapping[cache_path][-1].append(block)
            last_cache_path = cache_path
    return cache_mapping


def find_traceback(
    console_output: list[ConsoleInput | ConsoleOutput | Extension],
) -> str:
    for item in reversed(console_output):
        if not isinstance(item, ConsoleOutput):
            continue
        # There could be non-traceback output before the traceback appears.
        lines = item.string.splitlines()
        while lines:
            if lines[0].startswith("Traceback (most recent call last):"):
                break
            lines.pop(0)
        if lines:
            return "\n".join(lines) + "\n"
    return ""


@contextlib.contextmanager
def console_context(
    *, extensions, namespace=None, setup_lines=None, teardown_lines=None, document=None
) -> Generator[Console, None, None]:
    console = Console(extensions=extensions, namespace=namespace)
    console_output, errored = console.interpret(setup_lines or [])
    if errored:
        raise ConsoleError(find_traceback(console_output), document)
    try:
        yield console
    finally:
        console.resetbuffer()
        console_output, errored = console.interpret(teardown_lines or [])
        if errored:
            raise ConsoleError(find_traceback(console_output), document)


def interpret_code_blocks(
    blocks: list[
        doctest_block
        | literal_block
        | uqbar_book_defaults_block
        | uqbar_book_import_block
    ],
    *,
    allow_exceptions=False,
    document=None,
    extensions=None,
    namespace=None,
    setup_lines=None,
    teardown_lines=None,
    logger_func=None,
    use_black=False,
):
    results = {}
    block = blocks[0] if blocks else None
    with console_context(
        document=document,
        extensions=extensions,
        namespace=namespace,
        setup_lines=setup_lines,
        teardown_lines=teardown_lines,
    ) as console:
        default_proxy_options = {}
        for block in blocks:
            if isinstance(block, uqbar_book_defaults_block):
                default_proxy_options = dict(block.attlist())
                continue
            else:
                proxy_options = {**default_proxy_options, **dict(block.attlist())}
                console.push_proxy_options(proxy_options)
            if isinstance(block, uqbar_book_import_block):
                console_output, errored, has_exception = interpret_import_block(
                    console, block
                )
            elif isinstance(block, (literal_block, doctest_block)):
                console_output, errored, has_exception = interpret_literal_block(
                    console, block, use_black=use_black
                )
            if errored:
                traceback = find_traceback(console_output)
                if logger_func:
                    logger_func(traceback)
                if not (
                    block.get("allow-exceptions") or allow_exceptions or has_exception
                ):
                    raise ConsoleError(traceback, block)
            if block.get("hide"):
                console_output = [
                    _
                    for _ in console_output
                    if not isinstance(_, (ConsoleInput, ConsoleOutput))
                ]
            results[block] = console_output
    return results


def interpret_code_blocks_with_cache(
    blocks: list[
        doctest_block
        | literal_block
        | uqbar_book_defaults_block
        | uqbar_book_import_block
    ],
    *,
    cache_path,
    connection,
    allow_exceptions=False,
    document=None,
    extensions=None,
    namespace=None,
    setup_lines=None,
    teardown_lines=None,
    use_black=False,
):
    cache_data = query_cache_db(connection, cache_path)
    if cache_data is not None:
        local_node_mapping = dict(zip(blocks, cache_data))
    else:
        local_node_mapping = interpret_code_blocks(
            blocks,
            allow_exceptions=allow_exceptions,
            document=document,
            extensions=extensions,
            namespace=namespace,
            setup_lines=setup_lines,
            teardown_lines=teardown_lines,
            use_black=use_black,
        )
        if cache_path is not None:
            cache_data = list(local_node_mapping.values())
            update_cache_db(connection, cache_path, cache_data)
    return local_node_mapping


def interpret_import_block(
    console: Console, block: uqbar_book_import_block
) -> tuple[list[ConsoleInput | ConsoleOutput | Extension], bool, bool]:
    code_address = block["path"]
    module_name, sep, attr_name = code_address.rpartition(":")
    module = importlib.import_module(module_name)
    attr = getattr(module, attr_name)
    source = inspect.getsource(attr)
    lines = [f"from {module_name} import {attr_name}"]
    output, errored = console.interpret(lines)
    output = [ConsoleOutput(string=source)]
    return output, errored, False


def interpret_literal_block(
    console: Console, block: doctest_block | literal_block, use_black: bool = False
) -> tuple[list[ConsoleInput | ConsoleOutput | Extension], bool, bool]:
    has_exception = False
    lines = []
    contents = block[0]
    if isinstance(contents, (doctest_block, literal_block)):
        contents = contents[0]
    assert isinstance(contents, str)
    for line in contents.splitlines():
        if line.startswith((">>> ", "... ")):
            lines.append(line[4:])
        elif line.rstrip() == "...":
            lines.append("")
        elif line.startswith("Traceback (most recent call last):"):
            has_exception = True
    if use_black:
        try:
            lines = black_format(lines)
        except Exception:
            raise ConsoleError(traceback.format_exc(), block)
    console_output, errored = console.interpret(lines)
    return console_output, errored, has_exception


def literal_block_to_cache_path(block: literal_block) -> str | None:
    desc = None
    parent = block.parent
    while desc is None and parent is not None:
        if parent.tagname == "desc":
            desc = parent
            break
        else:
            parent = parent.parent
    if desc is None:
        return None
    desc_signature_node = desc[0]
    assert isinstance(desc_signature_node, desc_signature)
    module_path = desc_signature_node.attributes["module"]
    object_path = desc_signature_node.attributes["fullname"]
    id_path = desc_signature_node.attributes["ids"][0]
    module = importlib.import_module(module_path)
    outer = inner = module
    for path in object_path.split("."):
        outer = inner
        inner = getattr(outer, path)
    if isinstance(outer, type):
        _, _, attr_name = object_path.rpartition(".")
        try:
            attr = {attr.name: attr for attr in inspect.classify_class_attrs(outer)}[
                attr_name
            ]
        except KeyError:
            return id_path
        if attr.defining_class is not outer:
            return ".".join(
                [
                    attr.defining_class.__module__,
                    attr.defining_class.__name__,
                    attr_name,
                ]
            )
    return id_path


def parse_rst(rst_string: str) -> document:
    parser = Parser()
    # for name, class_ in []:  # Add custom directives here
    #     register_directive(name, class_)
    settings = get_default_settings(Parser)
    document = new_document("test", settings)
    parser.parse(rst_string, document)
    document = parser.document
    return document


def rebuild_document(document: document, node_mapping) -> None:
    for old_node, replacements in reversed(tuple(node_mapping.items())):
        new_nodes = []
        for is_vanilla, grouper in itertools.groupby(
            replacements, lambda x: isinstance(x, (ConsoleInput, ConsoleOutput))
        ):
            if is_vanilla:
                text = next(grouper).string
                for item in grouper:
                    if isinstance(item, ConsoleInput):
                        new_nodes.append(literal_block(text, text))
                        text = item.string
                    else:
                        text += item.string
                new_nodes.append(literal_block(text, text))
            else:
                for replacement in grouper:
                    new_nodes.extend(replacement.to_docutils())
        old_node.parent.replace(old_node, new_nodes)
