import collections
import importlib
import inspect
import itertools
import pickle
import sqlite3

from docutils.frontend import OptionParser
from docutils.nodes import Element, General, doctest_block, literal_block
from docutils.parsers.rst import Directive, Parser, directives
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
except ImportError:
    black = None


class UqbarBookDirective(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "allow-exceptions": directives.flag,
        "hide": directives.flag,
    }

    def run(self):
        self.assert_has_content()
        code = "\n".join(self.content)
        literal = literal_block(code, code)
        literal.line = self.content_offset  # set the content line number
        block = uqbar_book_block(code, literal)
        for key in (
            "allow-exceptions",
            "hide",
        ):
            if key in self.options:
                block[key] = True
        for key, spec in self.option_spec.items():
            option = self.options.get(key, None)
            if option is None:
                continue
            if spec == directives.flag:
                option = True
            block[key] = option
        set_source_info(self, block)
        return [block]


class UqbarBookSkipLiteralsDirective(Directive):
    has_content = False
    required_arguments = 0
    optional_arguments = 0

    def run(self):
        return [uqbar_book_skip_literals()]


class uqbar_book_block(General, Element):
    pass


class uqbar_book_skip_literals(General, Element):
    pass


def attr_path_to_defining_path(path):
    class_path, _, attr_name = path.rpartition(".")
    module_path, _, class_name = class_path.rpartition(".")
    module = None
    while module is None:
        try:
            module = importlib.import_module(module_path)
        except ModuleNotFoundError:
            module_path, _, outer_class_name = module_path.rpartition(".")
            class_name = outer_class_name + "." + class_name
    class_ = module
    for name in class_name.split("."):
        class_ = getattr(class_, name)
    attr = {attr.name: attr for attr in inspect.classify_class_attrs(class_)}[attr_name]
    if attr.defining_class is not class_:
        return ".".join(
            [attr.defining_class.__module__, attr.defining_class.__name__, attr_name]
        )
    return path


def collect_literal_blocks(document, skip_literals=False):
    prototype = (literal_block, doctest_block, uqbar_book_block)
    blocks = []
    for block in document.traverse(lambda node: isinstance(node, prototype)):
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


def interpret_code_blocks(
    blocks,
    allow_exceptions=False,
    extensions=None,
    namespace=None,
    setup_lines=None,
    teardown_lines=None,
    logger_func=None,
    use_black=False,
):
    results = collections.OrderedDict()
    console = Console(extensions=extensions, namespace=namespace)
    try:
        if setup_lines:
            console_output, errored = console.interpret(setup_lines)
            if errored:
                raise ConsoleError(console_output)
        for block in blocks:
            console.push_proxy_options(dict(block.attlist()))
            lines = []
            has_exception = False
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
            if use_black and black:
                mode = black.FileMode(
                    line_length=80, target_versions=[black.TargetVersion.PY36]
                )
                lines = black.format_str("\n".join(lines), mode=mode).splitlines()
            console_output, errored = console.interpret(lines)
            if errored:
                error_summary = None
                for i, item in enumerate(console_output):
                    if not isinstance(item, ConsoleOutput):
                        continue
                    output_lines = item.string.strip().splitlines()
                    if not output_lines[0].startswith(
                        "Traceback (most recent call last):"
                    ):
                        continue
                    error_summary = output_lines[-1]
                    break
                if logger_func:
                    logger_func(error_summary)
                if not (
                    block.get("allow-exceptions") or allow_exceptions or has_exception
                ):
                    raise ConsoleError(error_summary)
            if block.get("hide"):
                console_output = [
                    _
                    for _ in console_output
                    if not isinstance(_, (ConsoleInput, ConsoleOutput))
                ]
            results[block] = console_output
    except ConsoleError:
        raise ConsoleError(item.string, block)
    finally:
        if teardown_lines:
            console_output, errored = console.interpret(teardown_lines)
            if errored:
                raise ConsoleError(console_output)
    return results


def interpret_code_blocks_with_cache(
    blocks,
    cache_path,
    connection,
    allow_exceptions=False,
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
    name = desc_signature["names"][0]
    if desc_signature["class"]:
        return attr_path_to_defining_path(name)
    return name


def parse_rst(rst_string):
    parser = Parser()
    for name, class_ in []:  # Add custom directives here
        directives.register(name, class_)
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
