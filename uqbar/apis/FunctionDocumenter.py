import types
from uqbar.apis.MemberDocumenter import MemberDocumenter


class FunctionDocumenter(MemberDocumenter):
    """
    A basic documenter for functions.

    ::

        >>> import uqbar.apis
        >>> path = 'uqbar.io.walk'
        >>> documenter = uqbar.apis.FunctionDocumenter(path)
        >>> documentation = str(documenter)
        >>> print(documentation)
        .. autofunction:: walk

    :param package_path: the module path and name of the member to document
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Documenters'

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        return '.. autofunction:: {}'.format(
            self.client.__name__,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def validate_client(cls, client: object, module_path: str) -> bool:
        return (
            isinstance(client, types.FunctionType) and
            client.__module__ == module_path
            )

    ### PUBLIC PROPERTIES ###

    @property
    def documentation_section(self) -> str:
        return 'Functions'
