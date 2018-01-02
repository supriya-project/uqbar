import importlib
import pathlib
import types
from typing import Sequence, Tuple, Type
from uqbar.apis.ClassDocumenter import ClassDocumenter
from uqbar.apis.FunctionDocumenter import FunctionDocumenter
from uqbar.apis.MemberDocumenter import MemberDocumenter


class ModuleDocumenter:
    """
    A basic module documenter.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Documenters'

    ### INITIALIZER ###

    def __init__(
        self,
        package_path: str,
        document_private_members: bool=False,
        member_documenter_classes: Sequence[Type[MemberDocumenter]]=None,
        module_documenters: Sequence['ModuleDocumenter']=None,
        ):
        self._package_path = package_path

        client = importlib.import_module(package_path)
        assert isinstance(client, types.ModuleType)
        self._client = client

        self._document_private_members = bool(document_private_members)

        if member_documenter_classes is None:
            member_documenter_classes = [ClassDocumenter, FunctionDocumenter]
        for _ in member_documenter_classes:
            assert issubclass(_, MemberDocumenter), _
        self._member_documenter_classes = tuple(member_documenter_classes)

        if module_documenters is not None:
            for submodule_documenter in module_documenters:
                assert isinstance(submodule_documenter, type(self))
            module_documenters = tuple(module_documenters)
        self._module_documenters = module_documenters or ()

        self._member_documenters = self._populate()

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        result = self.build_preamble()
        result.extend(self.build_toc())
        for documenter in self._member_documenters:
            result.extend(['', str(documenter)])
        return '\n'.join(result)

    ### PRIVATE METHODS ###

    def _populate(self) -> None:
        documenters = []
        for name in sorted(dir(self.client)):
            if name.startswith('_') and not self.document_private_members:
                continue
            client = getattr(self.client, name)
            for class_ in self.member_documenter_classes:
                if class_.validate_client(client, self.package_path):
                    path = '{}.{}'.format(client.__module__, client.__name__)
                    documenter = class_(path)
                    documenters.append(documenter)
                    break
        return tuple(documenters)

    ### PUBLIC METHODS ###

    def build_preamble(self) -> Sequence[str]:
        return [
            '.. _{}:'.format(self.reference_name),
            '',
            self.package_name,
            '=' * len(self.package_name),
            '',
            '.. automodule:: {}'.format(self.package_path),
            '',
            '.. currentmodule:: {}'.format(self.package_path),
            ]

    def build_toc(
        self,
        hidden: bool=False,
        include_modules: bool=True,
        ) -> Sequence[str]:
        result = []
        if not self.module_documenters:
            return result
        result.extend(['', '.. toctree::'])
        if hidden:
            result.append('   :hidden:')
        result.append('')
        for submodule_documenter in self.module_documenters or []:
            if (
                not submodule_documenter.is_package and
                not include_modules
                ):
                continue
            path = submodule_documenter.package_path
            path = path[len(self.package_path) + 1:]
            if submodule_documenter.is_package:
                path = '{}/index'.format(path)
            result.append('   {}'.format(path))
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def client(self) -> object:
        return self._client

    @property
    def is_package(self) -> bool:
        return hasattr(self.client, '__path__')

    @property
    def document_private_members(self) -> bool:
        return self._document_private_members

    @property
    def documentation_path(self) -> pathlib.Path:
        path = pathlib.Path('.').joinpath(*self.package_path.split('.'))
        if self.is_package:
            path = path.joinpath('index')
        return path.with_suffix('.rst')

    @property
    def is_nominative(self) -> bool:
        if self.is_package or len(self.member_documenters) != 1:
            return False
        parts = self.member_documenters[0].package_path.split('.')
        return parts[-1] == parts[-2]

    @property
    def member_documenter_classes(self) -> Sequence[
        Type[MemberDocumenter]]:
        return self._member_documenter_classes

    @property
    def member_documenters(self) -> Sequence[MemberDocumenter]:
        return self._member_documenters

    @property
    def member_documenters_by_section(self) -> Sequence[
        Tuple[str, Sequence[MemberDocumenter]]]:
        result = {}
        for documenter in self.member_documenters:
            result.setdefault(
                documenter.documentation_section, []).append(documenter)
        return sorted(result.items())

    @property
    def module_documenters(self) -> Sequence['ModuleDocumenter']:
        return self._module_documenters

    @property
    def package_name(self) -> str:
        if '.' in self.package_path:
            return self._package_path.rpartition('.')[-1]
        return self._package_path

    @property
    def package_path(self) -> str:
        return self._package_path

    @property
    def reference_name(self) -> str:
        return self.package_path \
            .replace('_', '-') \
            .replace('.', '--')
