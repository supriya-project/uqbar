import abc
import ast
import code
import contextlib
import importlib
import inspect
import itertools
import logging
import pickle
import sqlite3
import subprocess
import sys
import traceback
import types
from dataclasses import dataclass
from pathlib import Path
from typing import Any, AsyncGenerator, Callable, Dict, Union

from docutils.frontend import get_default_settings
from docutils.nodes import (
    Element,
    General,
    SkipNode,
    doctest_block,
    document,
    literal_block,
)
from docutils.parsers.rst import Directive, Parser
from docutils.parsers.rst.directives import flag, path
from docutils.utils import new_document
from sphinx.addnodes import desc_signature
from sphinx.util.nodes import set_source_info
from typing_extensions import ClassVar

from ..io import RedirectedStreams
from ..strings import ansi_escape

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


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ConsoleInput:
    string: str


@dataclass(frozen=True)
class ConsoleOutput:
    string: str


class ConsoleError(Exception):
    pass


unset = object()


class MonkeyPatch(object):
    def __init__(self) -> None:
        self._attributes: list[tuple[Any, str, Any]] = []

    def setattr(self, target: Any, name: str, value: Any = unset) -> None:
        oldval = getattr(target, name, unset)
        if inspect.isclass(target):
            oldval = target.__dict__.get(name, unset)
        self._attributes.append((target, name, oldval))
        setattr(target, name, value)

    def undo(self) -> None:
        for obj, name, value in reversed(self._attributes):
            if value is not unset:
                setattr(obj, name, value)
            else:
                delattr(obj, name)
        self._attributes[:] = []


class Console(code.InteractiveConsole):
    """
    Interactive console providing a sandboxed namespace for executing code
    examples.
    """

    ### INITIALIZER ###

    def __init__(
        self,
        namespace: dict[str, Any] | None = None,
        extensions: list["Extension"] | None = None,
    ) -> None:
        super().__init__(
            filename="<stdin>",
            locals={**(namespace or {}), "__name__": "__main__", "__package__": None},
        )
        self.compile.compiler.flags |= ast.PyCF_ALLOW_TOP_LEVEL_AWAIT
        self.extensions = extensions
        self.errored = False
        self.results: list[Any] = []
        self.monkeypatch = MonkeyPatch()
        self.proxy_options: dict[str, dict[str, Any]] = {}

    ### SPECIAL METHODS ###

    def __enter__(self) -> "Console":
        self.monkeypatch = MonkeyPatch()
        for extension in self.extensions or []:
            extension.setup_console(self, self.monkeypatch)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.monkeypatch.undo()
        for extension in self.extensions or []:
            extension.teardown_console(self)

    ### PRIVATE METHODS ###

    def _showtraceback(self, *args) -> None:
        """
        Re-implementation of code.InteractiveConsole's showtraceback().

        No new functionality, but placing it here prevents the addition of
        extra lines in the trace output when run under GHA.
        """
        sys.last_type, sys.last_value, last_tb = ei = sys.exc_info()
        sys.last_traceback = last_tb
        try:
            self.write(
                "".join(
                    traceback.format_exception(
                        ei[0], ei[1], last_tb.tb_next if last_tb else None
                    )
                )
            )
        finally:
            last_tb = ei = None  # type: ignore

    ### PUBLIC METHODS ###

    def flush(self) -> None:
        pass

    async def interpret(
        self, lines: list[str]
    ) -> tuple[list[Union[ConsoleInput, ConsoleOutput, "Extension"]], bool]:
        self.resetbuffer()
        self.errored = False
        self.results[:] = []
        is_incomplete_statement = False
        with RedirectedStreams(self, self), self:
            prompt = ">>> "
            for line_number, line in enumerate(lines, 1):
                self.results.append(ConsoleInput(prompt + line + "\n"))
                try:
                    is_incomplete_statement = await self.push_async(line)
                except SystemExit:
                    self.resetbuffer()
                prompt = "... " if is_incomplete_statement else ">>> "
            if is_incomplete_statement:
                self.results.append(ConsoleInput(prompt + "\n"))
                try:
                    is_incomplete_statement = await self.push_async("\n")
                except SystemExit:
                    self.resetbuffer()
            if is_incomplete_statement:
                self.errored = True
        results = []
        for class_, grouper in itertools.groupby(self.results, lambda x: type(x)):
            if class_ is ConsoleInput:
                # Strip extra blank lines induced by black.
                string = "".join(_.string for _ in grouper if _.string.strip() != ">>>")
                results.append(class_(string=string))
            elif class_ is ConsoleOutput:
                results.append(class_(string="".join(_.string for _ in grouper)))
            else:
                results.extend(grouper)
        return results, self.errored

    async def push_async(self, line, filename=None, _symbol="single") -> bool:
        self.buffer.append(line)
        source = "\n".join(self.buffer)
        if filename is None:
            filename = self.filename
        more = await self.runsource_async(source, filename, symbol=_symbol)
        if not more:
            self.resetbuffer()
        return more

    def push_proxy(self, proxy: "Extension") -> None:
        self.results.append(proxy)

    def push_proxy_options(self, options: dict | None = None) -> None:
        self.proxy_options = options or {}

    async def runcode_async(self, code) -> Any:
        func = types.FunctionType(code, self.locals)
        try:
            if inspect.iscoroutine(coro := func()):
                return await coro
            return coro
        except SystemExit:
            raise
        except BaseException:
            self.showtraceback()

    async def runsource_async(
        self, source, filename="<input>", symbol="single"
    ) -> bool:
        try:
            code = self.compile(source, filename, symbol)
        except (OverflowError, SyntaxError, ValueError):
            self.showsyntaxerror(filename, source=source)
            return False
        if code is None:
            return True
        await self.runcode_async(code)
        return False

    def showsyntaxerror(self, filename: str | None = None, *, source: str = "") -> None:
        super().showsyntaxerror(filename=filename, source=source)
        self.errored = True

    def showtraceback(self) -> None:
        self._showtraceback()
        self.errored = True

    def write(self, string: str) -> None:
        self.results.append(ConsoleOutput(string))


class Extension:
    @classmethod
    def add_option(cls, key, value) -> None:
        UqbarBookDirective.option_spec[key] = value
        UqbarBookDefaultsDirective.option_spec[key] = value

    @classmethod
    @abc.abstractmethod
    def setup_console(cls, console: Console, monkeypatch: MonkeyPatch) -> None:
        """
        Perform console setup tasks before executing a suite of code blocks,
        e.g. monkeypatching IO operations to allow media capture.
        """
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def setup_sphinx(cls, app) -> None:
        """
        Setup Sphinx, e.g. register custom nodes and visitors.
        """
        raise NotImplementedError

    @classmethod
    def teardown_console(cls, app) -> None:
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


class UqbarShellDirective(Directive):
    __documentation_ignore_inherited__ = True

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec: ClassVar[Dict[str, Any]] = {
        "cwd": path,
        "rel": path,
        "user": str,
        "host": str,
    }

    def run(self) -> list[literal_block]:
        self.assert_has_content()
        result: list[str] = []
        working_directory = Path.cwd()
        if cwd := self.options.get("cwd"):
            if (desired_directory := Path(cwd)).is_absolute():
                working_directory = desired_directory
            else:
                working_directory = Path.cwd() / desired_directory
        working_directory = working_directory.resolve()
        relative_directory: Path | None = None
        if rel := self.options.get("rel"):
            if (desired_directory := Path(rel)).is_absolute():
                relative_directory = desired_directory
            else:
                relative_directory = (Path.cwd() / desired_directory).resolve()
        user = self.options.get("user", "user")
        host = self.options.get("host", "host")
        path = working_directory.name
        if relative_directory:
            path = str(working_directory.relative_to(relative_directory.parent))
        for line in self.content:
            result.append(f"{user}@{host}:~/{path}$ {line}")
            result.append(
                ansi_escape(
                    subprocess.run(
                        line,
                        cwd=working_directory,
                        shell=True,
                        stderr=subprocess.STDOUT,
                        stdout=subprocess.PIPE,
                        text=True,
                    ).stdout
                )
            )
        code = "\n".join(result)
        block = literal_block(code, code)
        block.attributes["language"] = "console"
        block.line = self.content_offset
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


def query_cache_db(
    connection: sqlite3.Connection, cache_path: str
) -> list[list[ConsoleInput | ConsoleOutput | Extension]] | None:
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


def update_cache_db(
    connection: sqlite3.Connection,
    cache_path: str,
    data: list[list[ConsoleInput | ConsoleOutput | Extension]],
) -> None:
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


@contextlib.asynccontextmanager
async def console_context(
    *, extensions, namespace=None, setup_lines=None, teardown_lines=None, document=None
) -> AsyncGenerator[Console, None]:
    console = Console(extensions=extensions, namespace=namespace)
    console_output, errored = await console.interpret(setup_lines or [])
    if errored:
        raise ConsoleError(find_traceback(console_output), document)
    try:
        yield console
    finally:
        console.resetbuffer()
        console_output, errored = await console.interpret(teardown_lines or [])
        if errored:
            raise ConsoleError(find_traceback(console_output), document)


async def interpret_code_blocks(
    blocks: list[
        doctest_block
        | literal_block
        | uqbar_book_defaults_block
        | uqbar_book_import_block
    ],
    *,
    allow_exceptions: bool = False,
    document: document | None = None,
    extensions: list[Extension] | None = None,
    logger_func: Callable[[str], None] | None = None,
    namespace: dict[str, Any] | None = None,
    setup_lines: list[str] | None = None,
    teardown_lines: list[str] | None = None,
    use_black: bool = False,
) -> dict[
    doctest_block | literal_block | uqbar_book_defaults_block | uqbar_book_import_block,
    list[ConsoleInput | ConsoleOutput | Extension],
]:
    results: dict[
        doctest_block
        | literal_block
        | uqbar_book_defaults_block
        | uqbar_book_import_block,
        list[ConsoleInput | ConsoleOutput | Extension],
    ] = {}
    block = blocks[0] if blocks else None
    async with console_context(
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
                console_output, errored, has_exception = await interpret_import_block(
                    console, block
                )
            elif isinstance(block, (literal_block, doctest_block)):
                console_output, errored, has_exception = await interpret_literal_block(
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


async def interpret_code_blocks_with_cache(
    blocks: list[
        doctest_block
        | literal_block
        | uqbar_book_defaults_block
        | uqbar_book_import_block
    ],
    cache_path: str,
    connection: sqlite3.Connection,
    *,
    allow_exceptions: bool = False,
    document: document | None = None,
    extensions: list[Extension] | None = None,
    logger_func: Callable[[str], None] | None = None,
    namespace: dict[str, Any] | None = None,
    setup_lines: list[str] | None = None,
    teardown_lines: list[str] | None = None,
    use_black: bool = False,
) -> dict[
    doctest_block | literal_block | uqbar_book_defaults_block | uqbar_book_import_block,
    list[ConsoleInput | ConsoleOutput | Extension],
]:
    if (cache_data := query_cache_db(connection, cache_path)) is not None:
        return dict(zip(blocks, cache_data))
    local_node_mapping = await interpret_code_blocks(
        blocks,
        allow_exceptions=allow_exceptions,
        document=document,
        extensions=extensions,
        logger_func=logger_func,
        namespace=namespace,
        setup_lines=setup_lines,
        teardown_lines=teardown_lines,
        use_black=use_black,
    )
    if cache_path is not None:
        cache_data = list(local_node_mapping.values())
        update_cache_db(connection, cache_path, cache_data)
    return local_node_mapping


async def interpret_import_block(
    console: Console, block: uqbar_book_import_block
) -> tuple[list[ConsoleInput | ConsoleOutput | Extension], bool, bool]:
    code_address = block["path"]
    module_name, sep, attr_name = code_address.rpartition(":")
    module = importlib.import_module(module_name)
    attr = getattr(module, attr_name)
    source = inspect.getsource(attr)
    lines = [f"from {module_name} import {attr_name}"]
    output, errored = await console.interpret(lines)
    output = [ConsoleOutput(string=source)]
    return output, errored, False


async def interpret_literal_block(
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
    console_output, errored = await console.interpret(lines)
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
    for path_ in object_path.split("."):
        outer = inner
        inner = getattr(outer, path_)
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
