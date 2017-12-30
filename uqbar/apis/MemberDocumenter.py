import abc
import importlib


class MemberDocumenter(metaclass=abc.ABCMeta):

    ### INITIALIZER ###

    def __init__(self, package_path):
        module_path, _, client_name = package_path.rpartition(':')
        module = importlib.import_module(module_path)
        client = getattr(module, client_name)
        if not self.validate_client(client, module_path):
            message = 'Unexpected object: {}'.format(type(client))
            raise ValueError(message)
        self._client = client
        self._package_path = package_path.replace(':', '.')

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError

    ### PUBLIC METHODS ###

    @classmethod
    @abc.abstractmethod
    def validate_client(cls, client, module_path):
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        return self._client

    @property
    @abc.abstractmethod
    def documentation_section(self):
        raise NotImplementedError

    @property
    def package_path(self):
        return self._package_path
