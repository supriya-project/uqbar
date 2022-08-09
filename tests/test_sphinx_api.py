import pathlib

import pytest

from uqbar.strings import normalize


@pytest.mark.sphinx("text", testroot="uqbar-sphinx-api-1")
def test_sphinx_api_1(app, status, warning):
    app.build()
    index_source = pathlib.Path(app.srcdir) / "api" / "index.rst"
    assert index_source.exists()
    assert "build succeeded" in status.getvalue()
    assert "8 added, 0 changed, 0 removed" in status.getvalue()
    assert "0 added, 0 changed, 0 removed" not in status.getvalue()
    assert not warning.getvalue().strip()
    path = pathlib.Path(app.srcdir) / "_build" / "text" / "api" / "index.txt"
    assert normalize(path.read_text()) == normalize(
        """
        API
        ***

        * fake_package

          * enums

          * module

          * multi

            * one

            * two
        """
    )
    # Build again, confirm that nothing has changed.
    app.build()
    assert "0 added, 0 changed, 0 removed" in status.getvalue()


@pytest.mark.sphinx("text", testroot="uqbar-sphinx-api-2")
def test_sphinx_api_2(app, status, warning):
    app.build()
    index_source = pathlib.Path(app.srcdir) / "api" / "index.rst"
    assert index_source.exists()
    assert "build succeeded" in status.getvalue()
    assert "8 added, 0 changed, 0 removed" in status.getvalue()
    assert "0 added, 0 changed, 0 removed" not in status.getvalue()
    assert not warning.getvalue().strip()
    path = pathlib.Path(app.srcdir) / "_build" / "text" / "api" / "index.txt"
    assert normalize(path.read_text()) == normalize(
        """
        API
        ***

        -[ fake_package ]-

        -[ fake_package.enums ]-

        -[ Enumerations ]-

        +------------+--------------------------------------------------------------------------------------------+
        | "FakeEnum" | An enumeration.                                                                            |
        +------------+--------------------------------------------------------------------------------------------+

        -[ fake_package.module ]-

        -[ Classes ]-

        +------------+--------------------------------------------------------------------------------------------+
        | "ChildCla  |                                                                                            |
        | ss"        |                                                                                            |
        +------------+--------------------------------------------------------------------------------------------+
        | "PublicCl  |                                                                                            |
        | ass"       |                                                                                            |
        +------------+--------------------------------------------------------------------------------------------+

        -[ Functions ]-

        +------------+--------------------------------------------------------------------------------------------+
        | "public_f  |                                                                                            |
        | unction"   |                                                                                            |
        +------------+--------------------------------------------------------------------------------------------+

        -[ fake_package.multi ]-

        -[ Classes ]-

        +------------+--------------------------------------------------------------------------------------------+
        | "PublicCl  |                                                                                            |
        | ass"       |                                                                                            |
        +------------+--------------------------------------------------------------------------------------------+

        -[ Functions ]-

        +------------+--------------------------------------------------------------------------------------------+
        | "public_f  |                                                                                            |
        | unction"   |                                                                                            |
        +------------+--------------------------------------------------------------------------------------------+

        -[ fake_package.multi.one ]-

        -[ Classes ]-

        +------------+--------------------------------------------------------------------------------------------+
        | "PublicCl  |                                                                                            |
        | ass"       |                                                                                            |
        +------------+--------------------------------------------------------------------------------------------+

        -[ Functions ]-

        +------------+--------------------------------------------------------------------------------------------+
        | "public_f  |                                                                                            |
        | unction"   |                                                                                            |
        +------------+--------------------------------------------------------------------------------------------+

        -[ fake_package.multi.two ]-

        -[ Classes ]-

        +------------+--------------------------------------------------------------------------------------------+
        | "PublicCl  |                                                                                            |
        | ass"       |                                                                                            |
        +------------+--------------------------------------------------------------------------------------------+

        -[ Functions ]-

        +------------+--------------------------------------------------------------------------------------------+
        | "public_f  |                                                                                            |
        | unction"   |                                                                                            |
        +------------+--------------------------------------------------------------------------------------------+
        """
    )
    # Build again, confirm that nothing has changed.
    app.build()
    assert "0 added, 0 changed, 0 removed" in status.getvalue()
