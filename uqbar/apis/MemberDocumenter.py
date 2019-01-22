import abc
import importlib


class MemberDocumenter(metaclass=abc.ABCMeta):
    """
    Abstract base class for module member documenters.

    Member documenters generate reStructuredText output for classes, functions
    and other objects defined in modules. They also implement the logic for
    identifying which of those objects should be selected for documenting via
    their
    :py:meth:`~uqbar.apis.MemberDocumenter.MemberDocumenter.validate_client`
    method. Module documenters loop over their client module's dict and try
    each of their member documenter class' validation method against each dict
    member in turn in order to identify documentable content and associate it
    with a member documenter class.

    .. tip::

       Subclass :py:class:`~uqbar.apis.MemberDocumenter` to implement your own
       custom module member documentation output. You'll need to override
       :py:meth:`~uqbar.apis.MemberDocumenter.MemberDocumenter.validate_client`
       with custom identification logic, and provide your desired
       reStructuredText output via an overridden
       :py:meth:`~uqbar.apis.MemberDocumenter.MemberDocumenter.__str__`
       implementation.

    :param package_path: the module path and name of the member to document
    """

    ### INITIALIZER ###

    def __init__(self, package_path: str) -> None:
        module_path, _, client_name = package_path.rpartition(".")
        module = importlib.import_module(module_path)
        client = getattr(module, client_name)
        if not self.validate_client(client, module_path):
            message = "Unexpected object: {}".format(type(client))
            raise ValueError(message)
        self._client = client
        self._package_path = package_path

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    ### PUBLIC METHODS ###

    @classmethod
    @abc.abstractmethod
    def validate_client(cls, client: object, module_path: str) -> bool:
        """
        Check if the member documenter can document the provided client.

        :param client: the potential client to validate
        :param module_path: the package path of the module where the client was encountered
        """
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @property
    def client(self) -> object:
        return self._client

    @property
    @abc.abstractmethod
    def documentation_section(self) -> str:
        raise NotImplementedError

    @property
    def package_path(self) -> str:
        return self._package_path
