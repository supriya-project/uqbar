import collections
import contextlib
import importlib
import inspect
import itertools
import pickle
import sqlite3
from typing import Any, Dict

from docutils.frontend import OptionParser
from docutils.nodes import Element, General, doctest_block, literal_block
from docutils.parsers.rst import Directive, Parser
from docutils.parsers.rst.directives import flag, register_directive
from docutils.utils import new_document
from sphinx.util.nodes import set_source_info

from uqbar.book.console import (
    Console,
    ConsoleError,
    ConsoleInput,
    ConsoleOutput,
)

try:
    import black

    def black_format(lines):
        mode = black.FileMode(
            line_length=80, target_versions=[black.TargetVersion.PY36]
        )
        return black.format_str("\n".join(lines), mode=mode).splitlines()


except ImportError:

    def black_format(lines):
        return lines


class UqbarBookDirective(Directive):
    __documentation_ignore_inherited__ = True

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec: Dict[str, Any] = {
        "allow-exceptions": flag,
        "hide": flag,
    }

    def run(self):
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
    option_spec: Dict[str, Any] = {}

    def run(self):
        block = uqbar_book_defaults_block()
        for key, value in self.options.items():
            block[key] = value
        return [block]


class UqbarBookImportDirective(Directive):
    __documentation_ignore_inherited__ = True

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    option_spec = {
        "hide": flag,
    }

    def run(self):
        block = uqbar_book_import_block()
        block["path"] = self.arguments[0]
        block.line = self.content_offset  # set the content line number
        set_source_info(self, block)
        if "hide" in self.options:
            block["hide"] = True
        return [block]


class uqbar_book_defaults_block(General, Element):
    __documentation_ignore_inherited__ = True


class uqbar_book_import_block(General, Element):
    __documentation_ignore_inherited__ = True


def collect_literal_blocks(document):
    prototype = (
        literal_block,
        doctest_block,
        uqbar_book_defaults_block,
        uqbar_book_import_block,
    )
    blocks = []
    for block in document.traverse(lambda node: isinstance(node, prototype)):
        if not isinstance(block, (uqbar_book_defaults_block, uqbar_book_import_block)):
            contents = block[0]
            if isinstance(contents, literal_block):
                contents = contents[0]
            if not contents.strip().startswith(">>>"):
                continue
        blocks.append(block)
    return blocks


def create_cache_db(path):
    connection = sqlite3.connect(str(path))
    connection.execute("CREATE TABLE cache (path TEXT, data BLOB, hits NUMBER);")
    connection.commit()
    return connection


def query_cache_db(connection, cache_path):
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


def update_cache_db(connection, cache_path, data):
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


def find_traceback(console_output):
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


@contextlib.contextmanager
def console_context(
    *, extensions, namespace=None, setup_lines=None, teardown_lines=None, document=None
):
    console = Console(extensions=extensions, namespace=namespace)
    console_output, errored = console.interpret(setup_lines or [])
    if errored:
        raise ConsoleError(find_traceback(console_output), document)
    yield console
    console_output, errored = console.interpret(teardown_lines or [])
    if errored:
        raise ConsoleError(find_traceback(console_output), document)


def interpret_code_blocks(
    blocks,
    allow_exceptions=False,
    document=None,
    extensions=None,
    namespace=None,
    setup_lines=None,
    teardown_lines=None,
    logger_func=None,
    use_black=False,
):
    results = collections.OrderedDict()
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
                    console, block, use_black=use_black,
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
    blocks,
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
        local_node_mapping = collections.OrderedDict(zip(blocks, cache_data))
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


def interpret_import_block(console, block):
    code_address = block["path"]
    module_name, sep, attr_name = code_address.rpartition(":")
    module = importlib.import_module(module_name)
    attr = getattr(module, attr_name)
    source = inspect.getsource(attr)
    lines = [f"from {module_name} import {attr_name}"]
    _, errored = console.interpret(lines)
    output = [ConsoleOutput(string=source)]
    return output, errored, False


def interpret_literal_block(console, block, use_black=False):
    has_exception = False
    lines = []
    contents = block[0]
    if isinstance(contents, literal_block):
        contents = contents[0]
    for line in contents.splitlines():
        if line.startswith((">>> ", "... ")):
            lines.append(line[4:])
        elif line.rstrip() == "...":
            lines.append("")
        elif line.startswith("Traceback (most recent call last):"):
            has_exception = True
    if use_black:
        lines = black_format(lines)
    console_output, errored = console.interpret(lines)
    return console_output, errored, has_exception


def literal_block_to_cache_path(block):
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
    desc_signature = desc[0]
    module_path = desc_signature.attributes["module"]
    object_path = desc_signature.attributes["fullname"]
    id_path = desc_signature.attributes["ids"][0]
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


def parse_rst(rst_string):
    parser = Parser()
    for name, class_ in []:  # Add custom directives here
        register_directive(name, class_)
    settings = OptionParser(components=(Parser,)).get_default_values()
    document = new_document("test", settings)
    parser.parse(rst_string, document)
    document = parser.document
    return document


def rebuild_document(document, node_mapping):
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
