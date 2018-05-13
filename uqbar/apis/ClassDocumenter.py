import enum
import inspect
from typing import cast
from uqbar.apis.MemberDocumenter import MemberDocumenter


class ClassDocumenter(MemberDocumenter):
    """
    A basic class documenter.

    ::

        >>> import uqbar.apis
        >>> path = 'uqbar.apis.ClassDocumenter.ClassDocumenter'
        >>> documenter = uqbar.apis.ClassDocumenter(path)
        >>> documentation = str(documenter)
        >>> print(documentation)
        .. autoclass:: ClassDocumenter
           :members:
           :undoc-members:

    .. tip::

       Subclass :py:class:`~uqbar.apis.ClassDocumenter` to implement your own
       custom class documentation output. You'll need to provide your desired
       reStructuredText output via an overridden
       :py:meth:`~uqbar.apis.ClassDocumenter.ClassDocumenter.__str__`
       implementation.

       See :py:class:`~uqbar.apis.SummarizingClassDocumenter` for an example.

    :param package_path: the module path and name of the member to document
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Documenters'

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        name = getattr(self.client, '__name__')
        if issubclass(self.client, Exception):  # type: ignore
            return '.. autoexception:: {}'.format(name)
        return '\n'.join([
            '.. autoclass:: {}'.format(name),
            '   :members:',
            '   :undoc-members:',
            ])

    ### PUBLIC METHODS ###

    @classmethod
    def validate_client(cls, client: object, module_path: str) -> bool:
        return (
            isinstance(client, type) and
            getattr(client, '__module__') == module_path
            )

    ### PUBLIC PROPERTIES ###

    @property
    def documentation_section(self) -> str:
        client = cast(type, self.client)
        if hasattr(client, '__documentation_section__'):
            section = getattr(client, '__documentation_section__')
            if section is not None:
                return section
        if inspect.isabstract(client):
            return 'Abstract Classes'
        elif issubclass(client, enum.Enum):
            return 'Enumerations'
        elif issubclass(client, Exception):
            return 'Exceptions'
        return 'Classes'
