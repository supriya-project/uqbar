import os
import pathlib
import shutil
import sys

import pytest
import sphinx.errors

from uqbar.strings import ansi_escape, normalize

index_content = normalize(
    """
    Fake Docs
    *********

       >>> print("hello, world!");
       hello, world!

       >>> print("foo bar baz!");
       foo bar baz!

       >>> print("i'm on my own line too!");
       i'm on my own line too!

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

       digraph G {
           node_0;
           node_1;
           node_0 -> node_1;
       }

       0

       digraph G {
           node_0;
           node_1;
           node_2;
           node_0 -> node_1;
           node_1 -> node_2;
       }

       1

       digraph G {
           node_0;
           node_1;
           node_2;
           node_3;
           node_0 -> node_1;
           node_1 -> node_2;
           node_2 -> node_3;
       }

       2

       >>> print(format(g, "graphviz"))
       digraph G {
           node_0;
           node_1;
           node_2;
           node_3;
           node_0 -> node_1;
           node_1 -> node_2;
           node_2 -> node_3;
       }

    * API

      * "just_a_function()"

      * "GrandParent"

        * "GrandParent.one()"

        * "GrandParent.three()"

        * "GrandParent.two()"

      * "Parent"

        * "Parent.one()"

        * "Parent.three()"

        * "Parent.two()"

      * "Uncle"

        * "Uncle.one()"

        * "Uncle.three()"

        * "Uncle.two()"

      * "Child"

        * "Child.one()"

        * "Child.three()"

        * "Child.two()"

      * "Outer"

        * "Outer.Inner"

          * "Outer.Inner.inner_method()"

        * "Outer.outer_method()"

    * Directives
    """
)

api_content = normalize(
    """
    API
    ***

    fake.just_a_function()

       Just a function.

          >>> print("I am just a function.")
          I am just a function.

    Text:

       >>> print("I am text.")
       I am text.

    class fake.GrandParent

       A grand parent.

          >>> print("I am a grand parent.")
          I am a grand parent.

       one()

          Grand parent: one.

             >>> print("Grand parent: one.")
             Grand parent: one.

       three()

          Grand parent: three.

             >>> print("Grand parent: three.")
             Grand parent: three.

             >>> import uqbar.graphs
             >>> g = uqbar.graphs.Graph()
             >>> n1 = uqbar.graphs.Node()
             >>> n2 = uqbar.graphs.Node()
             >>> g.extend([n1, n2])
             >>> e = n1.attach(n2)

             >>> print(format(g, "graphviz"))
             digraph G {
                 node_0;
                 node_1;
                 node_0 -> node_1;
             }

             >>> uqbar.graphs.Grapher(g)()

             digraph G {
                 node_0;
                 node_1;
                 node_0 -> node_1;
             }

          And that, my friends, is a graph.

       two()

          Grand parent: two.

             >>> print("Grand parent: two.")
             Grand parent: two.

    Text:

       >>> print("I am text.")
       I am text.

    class fake.Parent

       A parent.

          >>> print("I am a parent.")
          I am a parent.

       one()

          Parent: one.

             >>> print("Parent: one.")
             Parent: one.

       three()

          Grand parent: three.

             >>> print("Grand parent: three.")
             Grand parent: three.

             >>> import uqbar.graphs
             >>> g = uqbar.graphs.Graph()
             >>> n1 = uqbar.graphs.Node()
             >>> n2 = uqbar.graphs.Node()
             >>> g.extend([n1, n2])
             >>> e = n1.attach(n2)

             >>> print(format(g, "graphviz"))
             digraph G {
                 node_0;
                 node_1;
                 node_0 -> node_1;
             }

             >>> uqbar.graphs.Grapher(g)()

             digraph G {
                 node_0;
                 node_1;
                 node_0 -> node_1;
             }

          And that, my friends, is a graph.

       two()

          Grand parent: two.

             >>> print("Grand parent: two.")
             Grand parent: two.

    Text:

       >>> print("I am text.")
       I am text.

    class fake.Uncle

       one()

          Grand parent: one.

             >>> print("Grand parent: one.")
             Grand parent: one.

       three()

          Grand parent: three.

             >>> print("Grand parent: three.")
             Grand parent: three.

             >>> import uqbar.graphs
             >>> g = uqbar.graphs.Graph()
             >>> n1 = uqbar.graphs.Node()
             >>> n2 = uqbar.graphs.Node()
             >>> g.extend([n1, n2])
             >>> e = n1.attach(n2)

             >>> print(format(g, "graphviz"))
             digraph G {
                 node_0;
                 node_1;
                 node_0 -> node_1;
             }

             >>> uqbar.graphs.Grapher(g)()

             digraph G {
                 node_0;
                 node_1;
                 node_0 -> node_1;
             }

          And that, my friends, is a graph.

       two()

          Grand parent: two.

             >>> print("Grand parent: two.")
             Grand parent: two.

    Text:

       >>> print("I am text.")
       I am text.

    class fake.Child

       A child.

          >>> print("I am a child.")
          I am a child.

       one()

          Parent: one.

             >>> print("Parent: one.")
             Parent: one.

       three()

          Grand parent: three.

             >>> print("Grand parent: three.")
             Grand parent: three.

             >>> import uqbar.graphs
             >>> g = uqbar.graphs.Graph()
             >>> n1 = uqbar.graphs.Node()
             >>> n2 = uqbar.graphs.Node()
             >>> g.extend([n1, n2])
             >>> e = n1.attach(n2)

             >>> print(format(g, "graphviz"))
             digraph G {
                 node_0;
                 node_1;
                 node_0 -> node_1;
             }

             >>> uqbar.graphs.Grapher(g)()

             digraph G {
                 node_0;
                 node_1;
                 node_0 -> node_1;
             }

          And that, my friends, is a graph.

       two()

          Child: two.

             >>> print("Child: two.")
             Child: two.

    Text:

       >>> print("I am text.")
       I am text.

    class fake.Outer

       An outer class.

          >>> print("I am an outer class.")
          I am an outer class.

       class Inner

          An inner class.

             >>> print("I am an inner class.")
             I am an inner class.

          inner_method()

             Inner: method.

                >>> print("Inner: method.")
                Inner: method.

       outer_method()

          Outer: method.

             >>> print("Outer: method.")
             Outer: method.
    """
)

directives_content = normalize(
    """
    Directives
    **********

       >>> value = 1

       >>> value += 1
       >>> value
       2

       class ChildClass(PublicClass):
           def inheritable_method(self):
               pass

           def new_method(self):
               pass

       >>> value += 1
       >>> value
       4

       >>> ChildClass.__name__
       'ChildClass'

       >>> 1 / 0
       Traceback (most recent call last):
         File "<stdin>", line 1, in <module>
       ZeroDivisionError: division by zero
    """
)


@pytest.fixture(autouse=True)
def test_path():
    path = pathlib.Path(__file__).parent / "roots" / "test-uqbar-sphinx-book"
    assert path.exists()
    sys.path.insert(0, str(path))
    yield
    sys.path.remove(str(path))


@pytest.fixture
def rm_dirs(app):
    path = pathlib.Path(app.doctreedir)
    shutil.rmtree(path)
    yield


@pytest.mark.sphinx(
    "html", testroot="uqbar-sphinx-book", confoverrides={"uqbar_book_use_cache": True}
)
def test_sphinx_book_html_cached(app, status, warning, rm_dirs):
    app.build()
    assert not warning.getvalue().strip()
    image_path = pathlib.Path(app.outdir) / "_images"
    dot_paths = [path for path in image_path.iterdir() if path.suffix == ".dot"]
    dot_sources = set(normalize(path.read_text()) for path in dot_paths)
    assert dot_sources == set(
        [
            normalize(
                """
                digraph G {
                    node_0;
                    node_1;
                    node_0 -> node_1;
                }
                """
            ),
            normalize(
                """
                digraph G {
                    node_0;
                    node_1;
                    node_2;
                    node_0 -> node_1;
                    node_1 -> node_2;
                }
                """
            ),
            normalize(
                """
                digraph G {
                    node_0;
                    node_1;
                    node_2;
                    node_3;
                    node_0 -> node_1;
                    node_1 -> node_2;
                    node_2 -> node_3;
                }
                """
            ),
        ]
    )
    for dot_path in dot_paths:
        assert dot_path.with_suffix(".svg").exists()


@pytest.mark.sphinx(
    "latex", testroot="uqbar-sphinx-book", confoverrides={"uqbar_book_use_cache": True}
)
def test_sphinx_book_latex_cached(app, status, warning, rm_dirs):
    app.build()
    assert not warning.getvalue().strip()


@pytest.mark.sphinx(
    "text", testroot="uqbar-sphinx-book", confoverrides={"uqbar_book_use_cache": True}
)
def test_sphinx_book_text_cached(app, status, warning, rm_dirs):
    app.build()
    assert not warning.getvalue().strip()
    assert app.config["uqbar_book_use_cache"]
    assert list(
        app.connection.execute("SELECT path, hits FROM cache ORDER BY path")
    ) == [
        ("fake.Child", 0),
        ("fake.Child.two", 0),
        ("fake.GrandParent", 0),
        ("fake.GrandParent.one", 1),
        ("fake.GrandParent.three", 3),
        ("fake.GrandParent.two", 2),
        ("fake.Outer", 0),
        ("fake.Outer.Inner", 0),
        ("fake.Outer.Inner.inner_method", 0),
        ("fake.Outer.outer_method", 0),
        ("fake.Parent", 0),
        ("fake.Parent.one", 1),
        ("fake.just_a_function", 0),
    ]
    assert not warning.getvalue().strip()
    for filename, expected_content in [
        ("api.txt", api_content),
        ("directives.txt", directives_content),
        ("index.txt", index_content),
    ]:
        path = pathlib.Path(app.srcdir) / "_build" / "text" / filename
        actual_content = normalize(path.read_text())
        assert actual_content == expected_content


@pytest.mark.sphinx(
    "text", testroot="uqbar-sphinx-book", confoverrides={"uqbar_book_use_cache": False}
)
def test_sphinx_book_text_uncached(app, status, warning, rm_dirs):
    app.build()
    assert not warning.getvalue().strip()
    assert not app.config["uqbar_book_use_cache"]
    for filename, expected_content in [
        ("api.txt", api_content),
        ("directives.txt", directives_content),
        ("index.txt", index_content),
    ]:
        path = pathlib.Path(app.srcdir) / "_build" / "text" / filename
        actual_content = normalize(path.read_text())
        assert actual_content == expected_content


@pytest.mark.sphinx("text", testroot="uqbar-sphinx-book-broken")
def test_sphinx_book_text_broken_strict(app, status, warning, rm_dirs):
    """
    Build halts.
    """
    with pytest.raises(sphinx.errors.ExtensionError):
        app.build()
    assert normalize(ansi_escape(status.getvalue())) == normalize(
        """
        Running Sphinx v{sphinx_version}
        [uqbar-book] initializing cache db
        building [mo]: targets for 0 po files that are out of date
        building [text]: targets for 1 source files that are out of date
        updating environment: [new config] 1 added, 0 changed, 0 removed
        reading sources... [100%] index
        """.format(
            sphinx_version=sphinx.__version__
        )
    )
    assert normalize(ansi_escape(warning.getvalue())) == normalize(
        """
        {srcdir}index.rst:15: WARNING:
            <literal_block xml:space="preserve">>>> print(this_name_does_not_exist)</literal_block>
            Traceback (most recent call last):
              File "<stdin>", line 1, in <module>
            NameError: name 'this_name_does_not_exist' is not defined
        """.format(
            srcdir=app.srcdir + os.path.sep
        )
    )


@pytest.mark.sphinx(
    "text",
    testroot="uqbar-sphinx-book",
    confoverrides={"uqbar_book_console_setup": ["1 / 0"]},
)
def test_sphinx_book_text_broken_setup(make_app, app_params):
    """
    Fail build immediately on console setup error.
    """
    args, kwargs = app_params
    with pytest.raises(sphinx.errors.ExtensionError):
        make_app(*args, **kwargs)


@pytest.mark.sphinx(
    "text",
    testroot="uqbar-sphinx-book",
    confoverrides={"uqbar_book_console_teardown": ["1 / 0"]},
)
def test_sphinx_book_text_broken_teardown(make_app, app_params):
    """
    Fail build immediately on console teardown error.
    """
    args, kwargs = app_params
    with pytest.raises(sphinx.errors.ExtensionError):
        make_app(*args, **kwargs)
