import sys

import pytest
from docutils.parsers.rst import directives

from uqbar.book import (
    ConsoleError,
    ConsoleInput,
    ConsoleOutput,
    UqbarBookDirective,
    collect_literal_blocks,
    interpret_code_blocks,
    parse_rst,
    rebuild_document,
)
from uqbar.book.extensions import GraphExtension
from uqbar.strings import normalize


@pytest.fixture(scope="module", autouse=True)
def register_directives():
    directives.register_directive("book", UqbarBookDirective)
    yield
    directives._directives.pop("book")


source_a = """
::

    >>> string = 'Hello, world!'

::

    >>> for i in range(3):
    ...     string += " {}".format(i)
    ...

::

    >>> print(string)
    Hello, world!
"""

source_b = """
::

    >>> import uqbar.graphs
    >>> g = uqbar.graphs.Graph()
    >>> n1 = uqbar.graphs.Node()
    >>> n2 = uqbar.graphs.Node()
    >>> g.extend([n1, n2])
    >>> e = n1.attach(n2)

::

    >>> print(format(g, "graphviz"))

::

    >>> uqbar.graphs.Grapher(g)()

"""


source_c = """
::

    >>> import uqbar.graphs
    >>> g = uqbar.graphs.Graph()
    >>> n1 = uqbar.graphs.Node()
    >>> g.append(n1)
    >>> for i in range(3):
    ...     n2 = uqbar.graphs.Node()
    ...     g.append(n2)
    ...     e = n1.attach(n2)
    ...     uqbar.graphs.Grapher(g)()
    ...     print(i)
    ...     n1 = n2
    ...

"""

source_d = """
..  book::
    :hide:

    >>> import uqbar.graphs
    >>> g = uqbar.graphs.Graph()
    >>> n1 = uqbar.graphs.Node()
    >>> n2 = uqbar.graphs.Node()
    >>> g.extend([n1, n2])
    >>> e = n1.attach(n2)
    >>> uqbar.graphs.Grapher(g)()

"""

source_e = """
::

    >>> async def hello_world():
    ...     print("Hello, world!")
    ...

::

    >>> await(hello_world())
    Hello, world!
"""


@pytest.mark.parametrize(
    "source, expected",
    [
        (
            source_a,
            """
            <document source="test">
                <literal_block xml:space="preserve">
                    >>> string = 'Hello, world!'
                <literal_block xml:space="preserve">
                    >>> for i in range(3):
                    ...     string += " {}".format(i)
                    ...
                <literal_block xml:space="preserve">
                    >>> print(string)
                    Hello, world!
            """,
        ),
        (
            source_b,
            """
            <document source="test">
                <literal_block xml:space="preserve">
                    >>> import uqbar.graphs
                    >>> g = uqbar.graphs.Graph()
                    >>> n1 = uqbar.graphs.Node()
                    >>> n2 = uqbar.graphs.Node()
                    >>> g.extend([n1, n2])
                    >>> e = n1.attach(n2)
                <literal_block xml:space="preserve">
                    >>> print(format(g, "graphviz"))
                <literal_block xml:space="preserve">
                    >>> uqbar.graphs.Grapher(g)()
            """,
        ),
    ],
)
def test_parse_rst(source: str, expected: str) -> None:
    document = parse_rst(source)
    assert normalize(document.pformat()) == normalize(expected)


@pytest.mark.parametrize(
    "source, expected",
    [
        (
            source_a,
            [
                """
                <literal_block xml:space="preserve">
                    >>> string = 'Hello, world!'
                """,
                """
                <literal_block xml:space="preserve">
                    >>> for i in range(3):
                    ...     string += " {}".format(i)
                    ...
                """,
                """
                <literal_block xml:space="preserve">
                    >>> print(string)
                    Hello, world!
                """,
            ],
        ),
        (
            source_b,
            [
                """
                <literal_block xml:space="preserve">
                    >>> import uqbar.graphs
                    >>> g = uqbar.graphs.Graph()
                    >>> n1 = uqbar.graphs.Node()
                    >>> n2 = uqbar.graphs.Node()
                    >>> g.extend([n1, n2])
                    >>> e = n1.attach(n2)
                """,
                """
                <literal_block xml:space="preserve">
                    >>> print(format(g, "graphviz"))
                """,
                """
                <literal_block xml:space="preserve">
                    >>> uqbar.graphs.Grapher(g)()
                """,
            ],
        ),
    ],
)
def test_collect_literal_blocks(source: str, expected: list[str]) -> None:
    document = parse_rst(source)
    blocks = collect_literal_blocks(document)
    actual = [normalize(block.pformat()) for block in blocks]
    expected = [normalize(text) for text in expected]
    assert actual == expected


@pytest.mark.asyncio
async def test_interpret_code_blocks_01() -> None:
    document = parse_rst(source_a)
    blocks = collect_literal_blocks(document)
    node_mapping = await interpret_code_blocks(blocks)
    assert list(node_mapping.values()) == [
        [ConsoleInput(string=">>> string = 'Hello, world!'\n")],
        [
            ConsoleInput(
                string='>>> for i in range(3):\n...     string += " {}".format(i)\n... \n'
            )
        ],
        [
            ConsoleInput(string=">>> print(string)\n"),
            ConsoleOutput(string="Hello, world! 0 1 2\n"),
        ],
    ]


@pytest.mark.asyncio
async def test_interpret_code_blocks_02() -> None:
    def logger_func(message):
        messages.append(message)

    error_message = (
        'Traceback (most recent call last):\n  File "<stdin>", line 1, in <module>\n'
    )
    if sys.version_info < (3, 7):
        error_message += "TypeError: must be str, not int\n"
    else:
        error_message += 'TypeError: can only concatenate str (not "int") to str\n'

    messages = []
    source = normalize(
        """
        This will interpret happily.

        ::

            >>> "1" + 2
            Traceback (most recent call last):
              File "<stdin>", line 1, in <module>
            {error_message}
        """.format(error_message=error_message)
    )
    document = parse_rst(source)
    blocks = collect_literal_blocks(document)
    # This has a traceback, so it passes.
    await interpret_code_blocks(blocks, logger_func=logger_func)
    assert messages == [error_message]
    messages[:] = []
    source = normalize(
        """
        This will not interpret happily.

        ::

            >>> for i in range(1, 4):
            ...     i / 0
            ...
            "This is fine"
        """
    )
    document = parse_rst(source)
    blocks = collect_literal_blocks(document)
    with pytest.raises(ConsoleError):
        # This does not have a traceback, so it fails.
        await interpret_code_blocks(blocks, logger_func=logger_func)
    assert messages == [
        (
            "Traceback (most recent call last):\n"
            '  File "<stdin>", line 2, in <module>\n'
            "ZeroDivisionError: division by zero\n"
        )
    ]
    messages[:] = []
    # This passes because we force it to.
    await interpret_code_blocks(blocks, allow_exceptions=True, logger_func=logger_func)
    assert messages == [
        (
            "Traceback (most recent call last):\n"
            '  File "<stdin>", line 2, in <module>\n'
            "ZeroDivisionError: division by zero\n"
        )
    ]


@pytest.mark.parametrize(
    "source, expected",
    [
        (
            source_a,
            """
            <document source="test">
                <literal_block xml:space="preserve">
                    >>> string = 'Hello, world!'
                <literal_block xml:space="preserve">
                    >>> for i in range(3):
                    ...     string += " {}".format(i)
                    ...
                <literal_block xml:space="preserve">
                    >>> print(string)
                    Hello, world! 0 1 2
            """,
        ),
        (
            source_b,
            """
            <document source="test">
                <literal_block xml:space="preserve">
                    >>> import uqbar.graphs
                    >>> g = uqbar.graphs.Graph()
                    >>> n1 = uqbar.graphs.Node()
                    >>> n2 = uqbar.graphs.Node()
                    >>> g.extend([n1, n2])
                    >>> e = n1.attach(n2)
                <literal_block xml:space="preserve">
                    >>> print(format(g, "graphviz"))
                    digraph G {
                        node_0;
                        node_1;
                        node_0 -> node_1;
                    }
                <literal_block xml:space="preserve">
                    >>> uqbar.graphs.Grapher(g)()
                <graphviz_block layout="dot" xml:space="preserve">
                    digraph G {
                        node_0;
                        node_1;
                        node_0 -> node_1;
                    }
            """,
        ),
        (
            source_c,
            """
            <document source="test">
                <literal_block xml:space="preserve">
                    >>> import uqbar.graphs
                    >>> g = uqbar.graphs.Graph()
                    >>> n1 = uqbar.graphs.Node()
                    >>> g.append(n1)
                    >>> for i in range(3):
                    ...     n2 = uqbar.graphs.Node()
                    ...     g.append(n2)
                    ...     e = n1.attach(n2)
                    ...     uqbar.graphs.Grapher(g)()
                    ...     print(i)
                    ...     n1 = n2
                    ...
                <graphviz_block layout="dot" xml:space="preserve">
                    digraph G {
                        node_0;
                        node_1;
                        node_0 -> node_1;
                    }
                <literal_block xml:space="preserve">
                    0
                <graphviz_block layout="dot" xml:space="preserve">
                    digraph G {
                        node_0;
                        node_1;
                        node_2;
                        node_0 -> node_1;
                        node_1 -> node_2;
                    }
                <literal_block xml:space="preserve">
                    1
                <graphviz_block layout="dot" xml:space="preserve">
                    digraph G {
                        node_0;
                        node_1;
                        node_2;
                        node_3;
                        node_0 -> node_1;
                        node_1 -> node_2;
                        node_2 -> node_3;
                    }
                <literal_block xml:space="preserve">
                    2
            """,
        ),
        (
            source_d,
            """
            <document source="test">
                <graphviz_block layout="dot" xml:space="preserve">
                    digraph G {
                        node_0;
                        node_1;
                        node_0 -> node_1;
                    }
            """,
        ),
        (
            source_e,
            """
            <document source="test">
                <literal_block xml:space="preserve">
                    >>> async def hello_world():
                    ...     print("Hello, world!")
                    ...
                <literal_block xml:space="preserve">
                    >>> await(hello_world())
                    Hello, world!
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_rebuild_document(source: str, expected: str) -> None:
    document = parse_rst(source)
    blocks = collect_literal_blocks(document)
    extensions = [GraphExtension]
    node_mapping = await interpret_code_blocks(blocks, extensions=extensions)
    rebuild_document(document, node_mapping)
    assert normalize(document.pformat()) == normalize(expected)
