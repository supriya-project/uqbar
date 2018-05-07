import pathlib
import pytest
from uqbar.strings import normalize


@pytest.mark.sphinx(
    'text',
    testroot='uqbar-sphinx-style',
    )
def test_sphinx_style_1(app, status, warning):
    app.build()
    assert 'build succeeded' in status.getvalue()
    assert not warning.getvalue().strip()
    path = (
        pathlib.Path(app.srcdir) / '_build' / 'text' /
        'api' / 'fake_package' / 'module.txt'
        )
    with path.open() as file_pointer:
        assert normalize(file_pointer.read()) == normalize('''
            module
            ******

            -[ Classes ]-

            class fake_package.module.ChildClass

               -[ Special methods ]-

               ("PublicClass").__str__()

                  Return str(self).

               -[ Methods ]-

               inheritable_method()

               ("PublicClass").method()

               new_method()

               ("PublicClass").other_method()

               -[ Class & static methods ]-

               classmethod ("PublicClass").class_method()

               static ("PublicClass").static_method(cls)

               -[ Read/write properties ]-

               ("PublicClass").read_write_property

               -[ Read-only properties ]-

               ("PublicClass").read_only_property

            class fake_package.module.PublicClass

               -[ Special methods ]-

               __str__()

                  Return str(self).

               -[ Methods ]-

               inheritable_method()

               method()

               other_method()

               -[ Class & static methods ]-

               classmethod class_method()

               static static_method(cls)

               -[ Read/write properties ]-

               read_write_property

               -[ Read-only properties ]-

               read_only_property

            -[ Functions ]-

            fake_package.module.public_function()
            ''')
