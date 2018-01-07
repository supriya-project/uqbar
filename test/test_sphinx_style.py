import pytest


@pytest.mark.sphinx(
    'html',
    testroot='uqbar-sphinx-style',
    )
def test_sphinx_style_1(app, status, warning):
    app.build()
    assert 'build succeeded' in status.getvalue()
    assert not warning.getvalue().strip()
