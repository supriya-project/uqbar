import pathlib

import pytest

from uqbar.strings import normalize


@pytest.mark.sphinx("text", testroot="uqbar-sphinx-api")
def test_sphinx_api_1(app, status, warning):
    app.build()
    index_source = pathlib.Path(app.srcdir) / "api" / "index.rst"
    assert index_source.exists()
    assert "build succeeded" in status.getvalue()
    assert not warning.getvalue().strip()
    path = pathlib.Path(app.srcdir) / "_build" / "text" / "api" / "index.txt"
    with path.open() as file_pointer:
        assert normalize(file_pointer.read()) == normalize(
            """
            API
            ***

            * fake_package

              * module

              * multi

                * one

                * two
            """
        )
