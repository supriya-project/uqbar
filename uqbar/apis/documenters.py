import enum
import importlib
import inspect
import pathlib
import types
from typing import List, MutableMapping, Optional, Sequence, Tuple, Type, cast


class MemberDocumenter:
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
            message = f"Unexpected object: {client!r} from {module_path}"
            raise ValueError(message)
        self._client = client
        self._package_path = package_path

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        raise NotImplementedError

    ### PUBLIC METHODS ###

    @classmethod
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
    def documentation_section(self) -> str:
        raise NotImplementedError

    @property
    def package_path(self) -> str:
        return self._package_path


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


class ClassDocumenter(MemberDocumenter):
    """
    A basic class documenter.

    ::

        >>> import uqbar.apis
        >>> path = 'uqbar.apis.documenters.ClassDocumenter'
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

       See :py:class:`~uqbar.apis.documenters.SummarizingClassDocumenter` for an example.

    :param package_path: the module path and name of the member to document
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Documenters"

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        name = getattr(self.client, "__name__")
        if issubclass(self.client, Exception):  # type: ignore
            return ".. autoexception:: {}".format(name)
        return "\n".join(
            [".. autoclass:: {}".format(name), "   :members:", "   :undoc-members:"]
        )

    ### PUBLIC METHODS ###

    @classmethod
    def validate_client(cls, client: object, module_path: str) -> bool:
        return isinstance(client, type) and getattr(client, "__module__") == module_path

    ### PUBLIC PROPERTIES ###

    @property
    def documentation_section(self) -> str:
        client = cast(type, self.client)
        if hasattr(client, "__documentation_section__"):
            section = getattr(client, "__documentation_section__")
            if section is not None:
                return section
        if inspect.isabstract(client):
            return "Abstract Classes"
        elif issubclass(client, enum.Enum):
            return "Enumerations"
        elif issubclass(client, Exception):
            return "Exceptions"
        return "Classes"


class ModuleDocumenter:
    """
    A basic module documenter.

    ::

        >>> import uqbar.apis
        >>> documenter = uqbar.apis.ModuleDocumenter("uqbar.io")
        >>> print(str(documenter))
        .. _uqbar--io:
        <BLANKLINE>
        io
        ==
        <BLANKLINE>
        .. automodule:: uqbar.io
        <BLANKLINE>
        .. currentmodule:: uqbar.io
        <BLANKLINE>
        .. autoclass:: DirectoryChange
           :members:
           :undoc-members:
        <BLANKLINE>
        .. autoclass:: Profiler
           :members:
           :undoc-members:
        <BLANKLINE>
        .. autoclass:: RedirectedStreams
           :members:
           :undoc-members:
        <BLANKLINE>
        .. autoclass:: Timer
           :members:
           :undoc-members:
        <BLANKLINE>
        .. autofunction:: find_common_prefix
        <BLANKLINE>
        .. autofunction:: find_executable
        <BLANKLINE>
        .. autofunction:: open_path
        <BLANKLINE>
        .. autofunction:: relative_to
        <BLANKLINE>
        .. autofunction:: walk
        <BLANKLINE>
        .. autofunction:: write

    .. tip::

       Subclass :py:class:`~uqbar.apis.ModuleDocumenter` to implement your own
       custom module documentation output.
       You'll need to provide your desired reStructuredText output
       via an overridden
       :py:meth:`~uqbar.apis.ModuleDocumenter.ModuleDocumenter.__str__`
       implementation.

       See :py:class:`~uqbar.apis.SummarizingModuleDocumenter` for an example.

    :param package_path: the module path of the module to document
    :param document_private_members: whether to documenter private module members
    :param member_documenter_classes: a list of
        :py:class:`~uqbar.apis.MemberDocumenter` subclasses, defining what classes
        to use to identify and document module members
    :param module_documenters: a list of of documenters for submodules and
        subpackages of the documented module; these are generated by an
        :py:class:`~uqbar.apis.APIBuilder` instance rather than the module
        documenter directly
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Documenters"

    ### INITIALIZER ###

    def __init__(
        self,
        package_path: str,
        document_private_members: bool = False,
        member_documenter_classes: Optional[Sequence[Type[MemberDocumenter]]] = None,
        module_documenters: Optional[Sequence["ModuleDocumenter"]] = None,
    ) -> None:
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
                assert isinstance(submodule_documenter, ModuleDocumenter)
            module_documenters = tuple(module_documenters)
        self._module_documenters = module_documenters or ()
        self._member_documenters = self._populate()

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        result = self._build_preamble()
        result.extend(self._build_toc(self.module_documenters or []))
        for documenter in self._member_documenters:
            result.extend(["", str(documenter)])
        return "\n".join(result)

    ### PRIVATE METHODS ###

    def _populate(self) -> Sequence[MemberDocumenter]:
        documenters = []
        for name in sorted(dir(self.client)):
            if name.startswith("_") and not self.document_private_members:
                continue
            client = getattr(self.client, name)
            for class_ in self.member_documenter_classes:
                if class_.validate_client(client, self.package_path):
                    path = "{}.{}".format(client.__module__, client.__name__)
                    documenter = class_(path)
                    documenters.append(documenter)
                    break
        return tuple(documenters)

    ### PRIVATE METHODS ###

    def _build_toc(self, documenters, **kwargs) -> List[str]:
        result: List[str] = []
        if not documenters:
            return result
        result.extend(["", ".. toctree::"])
        result.append("")
        module_documenters = [_ for _ in documenters if isinstance(_, type(self))]
        for module_documenter in module_documenters:
            path = self._build_toc_path(module_documenter)
            if path:
                result.append("   {}".format(path))
        return result

    def _build_toc_path(self, documenter):
        path = documenter.package_path.partition(self.package_path + ".")[-1]
        base, _, name = path.rpartition(".")
        if name.lower() == "index":
            path = base + "._" + name
        if not isinstance(documenter, ModuleDocumenter):
            path = path.rpartition(".")[0]
        elif documenter.is_package:
            path += "/index"
        if path.lower() == "index":
            path = "_" + path
        return path

    def _build_preamble(self) -> List[str]:
        result: List[str] = [
            ".. _{}:".format(self.reference_name),
            "",
            self.package_name,
            "=" * len(self.package_name),
            "",
            ".. automodule:: {}".format(self.package_path),
            "",
            ".. currentmodule:: {}".format(self.package_path),
        ]
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def client(self) -> object:
        return self._client

    @property
    def is_package(self) -> bool:
        return hasattr(self.client, "__path__")

    @property
    def document_private_members(self) -> bool:
        return self._document_private_members

    @property
    def documentation_path(self) -> pathlib.Path:
        path = pathlib.Path(".").joinpath(*self.package_path.split("."))
        if self.is_package:
            path = path.joinpath("index")
        elif path.name.lower() == "index":
            name = path.name
            path = path.parent.joinpath("_" + name)
        return path.with_suffix(".rst")

    @property
    def is_nominative(self) -> bool:
        if self.is_package or len(self.member_documenters) != 1:
            return False
        parts = self.member_documenters[0].package_path.split(".")
        return parts[-1] == parts[-2]

    @property
    def member_documenter_classes(self) -> Sequence[Type[MemberDocumenter]]:
        return self._member_documenter_classes

    @property
    def member_documenters(self) -> Sequence[MemberDocumenter]:
        return self._member_documenters

    @property
    def member_documenters_by_section(
        self,
    ) -> Sequence[Tuple[str, Sequence[MemberDocumenter]]]:
        result: MutableMapping[str, List[MemberDocumenter]] = {}
        for documenter in self.member_documenters:
            result.setdefault(documenter.documentation_section, []).append(documenter)
        return sorted(result.items())

    @property
    def module_documenters(self) -> Sequence["ModuleDocumenter"]:
        return self._module_documenters

    @property
    def package_name(self) -> str:
        if "." in self.package_path:
            return self._package_path.rpartition(".")[-1]
        return self._package_path

    @property
    def package_path(self) -> str:
        return self._package_path

    @property
    def reference_name(self) -> str:
        return self.package_path.replace("_", "-").replace(".", "--")


class RootDocumenter:
    """
    A basic root documenter.

    This documenter generates only one reStructuredText document: the root API
    index page, which contains information about all of the modules traversed
    by an :py:class:`~uqbar.apis.APIBuilder`.

    Output is a basic `toctree` directive.

    ::

        >>> import uqbar.apis
        >>> documenter = uqbar.apis.RootDocumenter(
        ...     module_documenters=[
        ...         uqbar.apis.ModuleDocumenter('uqbar.io'),
        ...         uqbar.apis.ModuleDocumenter('uqbar.strings'),
        ...         ],
        ...     )
        >>> print(str(documenter))
        API
        ===
        <BLANKLINE>
        .. toctree::
        <BLANKLINE>
           uqbar/io
           uqbar/strings
        <BLANKLINE>

    .. tip::

       Subclass :py:class:`~uqbar.apis.RootDocumenter` to
       implement your own custom module documentation output.
       You'll need to provide your desired reStructuredText output
       via an overridden
       :py:meth:`~uqbar.apis.RootDocumenter.RootDocumenter.__str__`
       implementation.

       See :py:class:`~uqbar.apis.SummarizingRootDocumenter` for an example.

    :param module_documenters: a list of of documenters for modules and
        packages of the root documenter; these are generated by an
        :py:class:`~uqbar.apis.APIBuilder` instance rather than the module
        documenter directly
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Documenters"

    ### INITIALIZER ###

    def __init__(self, module_documenters=None, title="API"):
        import uqbar.apis

        if module_documenters is not None:
            assert all(
                isinstance(_, uqbar.apis.ModuleDocumenter) for _ in module_documenters
            ), module_documenters
            module_documenters = tuple(module_documenters)
        self._module_documenters = module_documenters or ()
        self._title = title

    ### SPECIAL METHODS ###

    def __str__(self):
        result = [self.title, "=" * len(self.title), ""]
        if self.module_documenters:
            result.extend([".. toctree::", ""])
            for module_documenter in self.module_documenters:
                path = module_documenter.package_path.replace(".", "/")
                if module_documenter.is_package:
                    path = "{}/index".format(path)
                result.append("   {}".format(path))
            result.append("")
        return "\n".join(result)

    ### PUBLIC PROPERTIES ###

    @property
    def documentation_path(self):
        return pathlib.Path("index.rst")

    @property
    def module_documenters(self):
        return self._module_documenters

    @property
    def title(self):
        return self._title
