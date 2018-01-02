import abc
import importlib


class MemberDocumenter(metaclass=abc.ABCMeta):
    """
    Abstract base class for module member documenters.

    :param package_path: the module path and name of the member to document
    """

    ### INITIALIZER ###

    def __init__(self, package_path: str):
        module_path, _, client_name = package_path.rpartition('.')
        module = importlib.import_module(module_path)
        client = getattr(module, client_name)
        if not self.validate_client(client, module_path):
            message = 'Unexpected object: {}'.format(type(client))
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
