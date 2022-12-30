import pathlib
import sys

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

            * "FakeEnum"

              * "FakeEnum.BAR"

              * "FakeEnum.BAZ"

              * "FakeEnum.FOO"

              * "FakeEnum.QUUX"

          * module

            * "ChildClass"

              * "ChildClass.inheritable_method()"

              * "ChildClass.new_method()"

            * "PublicClass"

              * "PublicClass.class_method()"

              * "PublicClass.inheritable_method()"

              * "PublicClass.method()"

              * "PublicClass.other_method()"

              * "PublicClass.read_only_property"

              * "PublicClass.read_write_property"

              * "PublicClass.static_method()"

            * "public_function()"

          * multi

            * one

              * "PublicClass"

              * "public_function()"

            * two

              * "PublicClass"

              * "public_function()"

            * "PublicClass"

            * "public_function()"
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
    path = pathlib.Path(app.srcdir) / "_build" / "text" / "api" / "index.txt"
    warnings = [line.strip() for line in warning.getvalue().splitlines()]
    if sys.version_info.minor < 11:
        assert not warnings
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
    else:
        assert len(warnings) == 2
        assert normalize(path.read_text()) == normalize(
            """
            API
            ***

            -[ fake_package ]-

            -[ fake_package.enums ]-

            -[ Enumerations ]-

            +------------+--------------------------------------------------------------------------------------------+
            | "FakeEnum" |                                                                                            |
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
