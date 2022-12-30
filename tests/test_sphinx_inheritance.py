import sys

import pytest


@pytest.mark.sphinx("html", testroot="uqbar-sphinx-style")
def test_sphinx_style_html(app, status, warning):
    app.build()
    assert "build succeeded" in status.getvalue()
    warnings = [line.strip() for line in warning.getvalue().splitlines()]
    if sys.version_info.minor < 11:
        assert not warnings
    else:
        assert len(warnings) == 2


@pytest.mark.sphinx("latex", testroot="uqbar-sphinx-style")
def test_sphinx_style_latex(app, status, warning):
    app.build()
    assert "build succeeded" in status.getvalue()
    warnings = [line.strip() for line in warning.getvalue().splitlines()]
    assert not warnings
