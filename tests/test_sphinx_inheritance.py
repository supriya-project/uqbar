import pytest


@pytest.mark.sphinx("html", testroot="uqbar-sphinx-style")
def test_sphinx_style_html(app, status, warning):
    app.build()
    assert "build succeeded" in status.getvalue()
    assert not warning.getvalue().strip()


@pytest.mark.sphinx("latex", testroot="uqbar-sphinx-style")
def test_sphinx_style_latex(app, status, warning):
    app.build()
    assert "build succeeded" in status.getvalue()
    assert not warning.getvalue().strip()
