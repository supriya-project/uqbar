import enum
import inspect
from uqbar.apis.MemberDocumenter import MemberDocumenter


class ClassDocumenter(MemberDocumenter):
    """
    A basic documenter for classes.

    ::

        >>> import uqbar.apis
        >>> path = 'uqbar.apis.ClassDocumenter:ClassDocumenter'
        >>> documenter = uqbar.apis.ClassDocumenter(path)
        >>> documentation = str(documenter)
        >>> print(documentation)
        .. autoclass:: ClassDocumenter
           :members:
           :undoc-members:
           :show-inheritance:

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Documenters'

    ### SPECIAL METHODS ###

    def __str__(self):
        return '\n'.join([
            '.. autoclass:: {}'.format(
                self.client.__name__,
                ),
            '   :members:',
            '   :undoc-members:',
            '   :show-inheritance:',
            ])

    ### PUBLIC METHODS ###

    @classmethod
    def validate_client(cls, client, module_path):
        return (
            isinstance(client, type) and
            client.__module__ == module_path
            )

    ### PUBLIC PROPERTIES ###

    @property
    def documentation_section(self):
        if hasattr(self.client, '__documentation_section__'):
            return self.client.__documentation_section__
        elif inspect.isabstract(self.client):
            return 'Abstract Classes'
        elif issubclass(self.client, enum.Enum):
            return 'Enumerations'
        elif issubclass(self.client, Exception):
            return 'Exceptions'
        return 'Classes'
