import types

from uqbar.apis.MemberDocumenter import MemberDocumenter


class FunctionDocumenter(MemberDocumenter):
    """
    A basic function documenter.

    ::

        >>> import uqbar.apis
        >>> path = 'uqbar.io.walk'
        >>> documenter = uqbar.apis.FunctionDocumenter(path)
        >>> documentation = str(documenter)
        >>> print(documentation)
        .. autofunction:: walk

    .. tip::

       Subclass :py:class:`~uqbar.apis.FunctionDocumenter` to
       implement your own custom module documentation output.
       You'll need to provide your desired reStructuredText output
       via an overridden
       :py:meth:`~uqbar.apis.FunctionDocumenter.FunctionDocumenter.__str__`
       implementation.

    :param package_path: the module path and name of the member to document
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Documenters"

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        return ".. autofunction:: {}".format(getattr(self.client, "__name__"))

    ### PUBLIC METHODS ###

    @classmethod
    def validate_client(cls, client: object, module_path: str) -> bool:
        return (
            isinstance(client, types.FunctionType) and client.__module__ == module_path
        )

    ### PUBLIC PROPERTIES ###

    @property
    def documentation_section(self) -> str:
        return "Functions"
