import code
import inspect
import itertools
import sys
import traceback
from dataclasses import dataclass
from typing import Any

from ..io import RedirectedStreams
from .extensions import Extension


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
    r"""
    Interactive console providing a sandboxed namespace for executing code
    examples.

    .. container:: example

        ::

            >>> from uqbar.book.console import Console
            >>> console = Console()
            >>> results, errored = console.interpret([
            ...     "x = 3",
            ...     "for i in range(3):",
            ...     "    print(i + x)",
            ...     "",
            ...     "quit()",  # SystemExit is captured
            ...     "print(2 + 2)",
            ... ])

        ::

            >>> for result in results:
            ...     print(result)
            ...
            ConsoleInput(string='>>> x = 3\n>>> for i in range(3):\n...     print(i + x)\n... \n')
            ConsoleOutput(string='3\n4\n5\n')
            ConsoleInput(string='>>> quit()\n>>> print(2 + 2)\n')
            ConsoleOutput(string='4\n')

        ::

            >>> print(errored)
            False

    .. container:: example

        The console maintains state across multiple ``interpret()`` calls:

        ::

            >>> results, errored = console.interpret(["x + 2"])
            >>> for result in results:
            ...     print(result)
            ...
            ConsoleInput(string='>>> x + 2\n')
            ConsoleOutput(string='5\n')

        ::

            >>> print(errored)
            False

    .. container:: example

        Errors are reported but do not propagate outside of the ``interpret()`` call:

        ::

            >>> results, errored = console.interpret(["1 / 0"])
            >>> for result in results:
            ...     print(result)
            ...
            ConsoleInput(string='>>> 1 / 0\n')
            ConsoleOutput(string='Traceback (most recent call last):\n  File "<stdin>", line 1, in <module>\nZeroDivisionError: division by zero\n')

        ::

            >>> print(errored)
            True

    .. container:: example

        Error reporting resets:

        ::

            >>> results, errored = console.interpret(["x += 5", "print(x)"])
            >>> for result in results:
            ...     print(result)
            ...
            ConsoleInput(string='>>> x += 5\n>>> print(x)\n')
            ConsoleOutput(string='8\n')

        ::

            >>> print(errored)
            False

    """

    ### INITIALIZER ###

    def __init__(
        self,
        namespace: dict[str, Any] | None = None,
        extensions: list[Extension] | None = None,
    ) -> None:
        super().__init__(
            filename="<stdin>",
            locals={**(namespace or {}), "__name__": "__main__", "__package__": None},
        )
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

    def _showtraceback(self) -> None:
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

    def interpret(
        self, lines: list[str]
    ) -> tuple[list[ConsoleInput | ConsoleOutput | Extension], bool]:
        self.resetbuffer()
        self.errored = False
        self.results[:] = []
        is_incomplete_statement = False
        with RedirectedStreams(self, self), self:
            prompt = ">>> "
            for line_number, line in enumerate(lines, 1):
                self.results.append(ConsoleInput(prompt + line + "\n"))
                try:
                    is_incomplete_statement = self.push(line)
                except SystemExit:
                    self.resetbuffer()
                prompt = "... " if is_incomplete_statement else ">>> "
            if is_incomplete_statement:
                self.results.append(ConsoleInput(prompt + "\n"))
                try:
                    is_incomplete_statement = self.push("\n")
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

    def push_proxy(self, proxy: Extension) -> None:
        self.results.append(proxy)

    def push_proxy_options(self, options: dict | None = None) -> None:
        self.proxy_options = options or {}

    def showsyntaxerror(self, filename: str | None = None, *, source: str = "") -> None:
        super().showsyntaxerror(filename=filename, source=source)
        self.errored = True

    def showtraceback(self) -> None:
        self._showtraceback()
        self.errored = True

    def write(self, string: str) -> None:
        self.results.append(ConsoleOutput(string))
