import code
import itertools
from typing import Any, Dict, List, Optional, Tuple

from _pytest.monkeypatch import MonkeyPatch
from dataclasses import dataclass

from uqbar.io import RedirectedStreams


@dataclass(frozen=True)
class ConsoleInput:
    string: str


@dataclass(frozen=True)
class ConsoleOutput:
    string: str


class ConsoleError(Exception):
    pass


# TODO: Implement non-captured setup/teardown lines


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

    ### CLASS VARIABLES ###

    ### INITIALIZER ###

    def __init__(self, namespace: Optional[Dict] = None, extensions: List[Any] = None):
        super().__init__(
            filename="<stdin>",
            locals={**(namespace or {}), "__name__": "__main__", "__package__": None},
        )
        self.extensions = extensions
        self.errored = False
        self.results: List[Any] = []
        self.monkeypatch = None

    ### SPECIAL METHODS ###

    def __enter__(self):
        self.monkeypatch = MonkeyPatch()
        for extension in self.extensions or []:
            extension.setup(self, self.monkeypatch)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.monkeypatch.undo()

    ### PUBLIC METHODS ###

    def flush(self) -> None:
        pass

    def interpret(self, lines: List[str]) -> Tuple[List[Any], bool]:
        self.resetbuffer()
        self.errored = False
        self.results[:] = []
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

    def push_proxy(self, proxy):
        self.results.append(proxy)

    def showsyntaxerror(self, filename: str = None) -> None:
        super().showsyntaxerror(filename=filename)
        self.errored = True

    def showtraceback(self) -> None:
        super().showtraceback()
        self.errored = True

    def write(self, string: str) -> None:
        self.results.append(ConsoleOutput(string))
