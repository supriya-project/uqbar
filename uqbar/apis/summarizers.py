import enum
import inspect
import textwrap
from typing import List, MutableMapping, Tuple, cast
from unittest import mock

from sphinx.ext.autosummary import extract_summary  # type: ignore
from sphinx.util.docutils import new_document  # type: ignore

from ..strings import normalize
from .documenters import (
    ClassDocumenter,
    MemberDocumenter,
    ModuleDocumenter,
    RootDocumenter,
)


class SummarizingClassDocumenter(ClassDocumenter):
    """
    A summarizing class documenter.

    Organizes class members by category, separated by category title and
    horizontal rule.

    Categories include:

    -  Special methods
    -  Methods
    -  Class and static methods
    -  Read/write properties
    -  Read-only properties

    ::

        >>> import uqbar.apis
        >>> path = 'uqbar.apis.summarizers.SummarizingClassDocumenter'
        >>> documenter = uqbar.apis.SummarizingClassDocumenter(path)
        >>> documentation = str(documenter)
        >>> print(documentation)
        .. autoclass:: SummarizingClassDocumenter
        <BLANKLINE>
           .. raw:: html
        <BLANKLINE>
              <hr/>
        <BLANKLINE>
           .. rubric:: Attributes Summary
              :class: class-header
        <BLANKLINE>
           .. autosummary::
              :nosignatures:
        <BLANKLINE>
              __str__
              ignored_special_methods
        <BLANKLINE>
           .. raw:: html
        <BLANKLINE>
              <hr/>
        <BLANKLINE>
           .. rubric:: Special methods
              :class: class-header
        <BLANKLINE>
           .. automethod:: SummarizingClassDocumenter.__str__
        <BLANKLINE>
           .. raw:: html
        <BLANKLINE>
              <hr/>
        <BLANKLINE>
           .. rubric:: Class & static methods
              :class: class-header
        <BLANKLINE>
           .. container:: inherited
        <BLANKLINE>
              .. automethod:: SummarizingClassDocumenter.validate_client
        <BLANKLINE>
           .. raw:: html
        <BLANKLINE>
              <hr/>
        <BLANKLINE>
           .. rubric:: Read-only properties
              :class: class-header
        <BLANKLINE>
           .. container:: inherited
        <BLANKLINE>
              .. autoattribute:: SummarizingClassDocumenter.client
        <BLANKLINE>
           .. container:: inherited
        <BLANKLINE>
              .. autoattribute:: SummarizingClassDocumenter.documentation_section
        <BLANKLINE>
           .. container:: inherited
        <BLANKLINE>
              .. autoattribute:: SummarizingClassDocumenter.package_path

    :param package_path: the module path and name of the member to document
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Documenters"

    ignored_special_methods: Tuple[str, ...] = (
        "__dict__",
        "__getattribute__",
        "__getnewargs__",
        "__getstate__",
        "__init__",
        "__reduce__",
        "__reduce_ex__",
        "__setstate__",
        "__sizeof__",
        "__subclasshook__",
        "fromkeys",
        "pipe_cloexec",
    )

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        name = getattr(self.client, "__name__")
        if issubclass(self.client, Exception):  # type: ignore
            return ".. autoexception:: {}".format(name)
        attributes = self._classify_class_attributes()
        (
            class_methods,
            data,
            methods,
            readonly_properties,
            readwrite_properties,
            special_methods,
            static_methods,
        ) = attributes
        result = [".. autoclass:: {}".format(name)]
        if issubclass(self.client, enum.Enum):  # type: ignore
            result.extend(["   :members:", "   :undoc-members:"])
        else:
            result.extend(self._build_member_autosummary(attributes))
        result.extend(
            self._build_attribute_section(
                special_methods, "automethod", "Special methods"
            )
        )
        result.extend(self._build_attribute_section(methods, "automethod", "Methods"))
        result.extend(
            self._build_attribute_section(
                sorted(class_methods + static_methods, key=lambda x: x.name),
                "automethod",
                "Class & static methods",
            )
        )
        result.extend(
            self._build_attribute_section(
                readwrite_properties, "autoattribute", "Read/write properties"
            )
        )
        result.extend(
            self._build_attribute_section(
                readonly_properties, "autoattribute", "Read-only properties"
            )
        )
        return "\n".join(result)

    ### PRIVATE METHODS ###

    def _build_attribute_section(
        self, attributes, directive: str, title: str
    ) -> List[str]:
        result: List[str] = []
        if not attributes:
            return result
        result.extend(
            [
                "",
                "   .. raw:: html",
                "",
                "      <hr/>",
                "",
                "   .. rubric:: {}".format(title),
                "      :class: class-header",
            ]
        )
        for attribute in attributes:
            result.append("")
            autodoc_directive = "   .. {}:: {}.{}".format(
                directive, getattr(self.client, "__name__"), attribute.name
            )
            if attribute.defining_class is self.client:
                result.append(autodoc_directive)
            else:
                result.append("   .. container:: inherited")
                result.append("")
                result.append("   {}".format(autodoc_directive))
        return result

    def _build_member_autosummary(self, attributes) -> List[str]:
        result: List[str] = []
        all_attributes: List[inspect.Attribute] = []
        for attribute_section in attributes:
            all_attributes.extend(
                attribute
                for attribute in attribute_section
                if attribute.defining_class is self.client
            )
        all_attributes.sort(key=lambda x: x.name)
        if not all_attributes:
            return result
        result.extend(
            [
                "",
                "   .. raw:: html",
                "",
                "      <hr/>",
                "",
                "   .. rubric:: {}".format("Attributes Summary"),
                "      :class: class-header",
                "",
                "   .. autosummary::",
                "      :nosignatures:",
                "",
            ]
        )
        for attribute in all_attributes:
            result.append("      {}".format(attribute.name))
        return result

    def _classify_class_attributes(self):
        class_methods = []
        data = []
        methods = []
        readonly_properties = []
        readwrite_properties = []
        special_methods = []
        static_methods = []
        attrs = inspect.classify_class_attrs(self.client)
        for attr in attrs:
            if attr.defining_class is object:
                continue
            elif (
                getattr(self.client, "__documentation_ignore_inherited__", None)
                and attr.defining_class is not self.client
            ):
                continue
            # Handle un-gettable attrs like Flask-SQLAlchemy's Model's `query`
            try:
                getattr(self.client, attr.name)
            except Exception:
                continue
            if attr.kind == "method":
                if attr.name not in self.ignored_special_methods:
                    if attr.name.startswith("__"):
                        special_methods.append(attr)
                    elif not attr.name.startswith("_"):
                        methods.append(attr)
            elif attr.kind == "class method":
                if attr.name not in self.ignored_special_methods:
                    if attr.name.startswith("__"):
                        special_methods.append(attr)
                    elif not attr.name.startswith("_"):
                        class_methods.append(attr)
            elif attr.kind == "static method":
                if attr.name not in self.ignored_special_methods:
                    if attr.name.startswith("__"):
                        special_methods.append(attr)
                    elif not attr.name.startswith("_"):
                        static_methods.append(attr)
            elif attr.kind == "property" and not attr.name.startswith("_"):
                if attr.object.fset is None:
                    readonly_properties.append(attr)
                else:
                    readwrite_properties.append(attr)
            elif (
                attr.kind == "data"
                and not attr.name.startswith("_")
                and attr.name not in getattr(self.client, "__slots__", ())
            ):
                data.append(attr)
        class_methods = tuple(sorted(class_methods))
        data = tuple(sorted(data))
        methods = tuple(sorted(methods))
        readonly_properties = tuple(sorted(readonly_properties))
        readwrite_properties = tuple(sorted(readwrite_properties))
        special_methods = tuple(sorted(special_methods))
        static_methods = tuple(sorted(static_methods))
        result = (
            class_methods,
            data,
            methods,
            readonly_properties,
            readwrite_properties,
            special_methods,
            static_methods,
        )
        return result


class SummarizingModuleDocumenter(ModuleDocumenter):
    """
    A summarizing module documenter.

    Organizes member documenters by their *documentation section*.

    Treats *nominative* submodule documenters (almost) as if they were locally
    defined members. This means that a documenter for a package which contains
    a module which contains *only* one class or function named identically to
    that module will treat that class or function as though it was defined in
    the package's ``__init__.py``. These nominative submodule members are
    organized in each documentation section via an *autosummary* table, rather
    than including their documentation directly.

    ::

        >>> import uqbar.apis
        >>> documenter = uqbar.apis.SummarizingModuleDocumenter("uqbar.io")
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
        .. container:: svg-container
        <BLANKLINE>
           .. inheritance-diagram:: uqbar
              :lineage: uqbar.io
        <BLANKLINE>
        .. raw:: html
        <BLANKLINE>
           <hr/>
        <BLANKLINE>
        .. rubric:: Classes
           :class: section-header
        <BLANKLINE>
        .. autosummary::
           :nosignatures:
        <BLANKLINE>
           ~DirectoryChange
           ~Profiler
           ~RedirectedStreams
           ~Timer
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
        .. raw:: html
        <BLANKLINE>
           <hr/>
        <BLANKLINE>
        .. rubric:: Functions
           :class: section-header
        <BLANKLINE>
        .. autosummary::
           :nosignatures:
        <BLANKLINE>
           ~find_common_prefix
           ~find_executable
           ~open_path
           ~relative_to
           ~walk
           ~write
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

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        result = self._build_preamble()
        package_path = self.package_path.partition(".")[0]
        lineage_path = self.package_path
        result.extend(
            [
                "",
                ".. container:: svg-container",
                "",
                "   .. inheritance-diagram:: {}".format(package_path),
                "      :lineage: {}".format(lineage_path),
            ]
        )
        if self.is_nominative:
            result.extend(["", str(self.member_documenters[0])])
        else:
            if self.is_package:
                subpackage_documenters = [
                    _
                    for _ in self.module_documenters or []
                    if _.is_package or not _.is_nominative
                ]
                if subpackage_documenters:
                    result.extend(
                        [
                            "",
                            ".. raw:: html",
                            "",
                            "   <hr/>",
                            "",
                            ".. rubric:: Subpackages",
                            "   :class: section-header",
                        ]
                    )
                    result.extend(
                        self._build_toc(subpackage_documenters, show_full_paths=True)
                    )
            for section, documenters in self.member_documenters_by_section:
                result.extend(
                    [
                        "",
                        ".. raw:: html",
                        "",
                        "   <hr/>",
                        "",
                        ".. rubric:: {}".format(section),
                        "   :class: section-header",
                    ]
                )
                local_documenters = [
                    documenter
                    for documenter in documenters
                    if documenter.client.__module__ == self.package_path
                ]
                result.extend(self._build_toc(documenters))
                for local_documenter in local_documenters:
                    result.extend(["", str(local_documenter)])
        return "\n".join(result)

    ### PRIVATE METHODS ###

    def _build_toc(
        self, documenters, show_full_paths: bool = False, **kwargs
    ) -> List[str]:
        result: List[str] = []
        if not documenters:
            return result
        toctree_paths = set()
        for documenter in documenters:
            path = self._build_toc_path(documenter)
            if path:
                toctree_paths.add(path)
        if toctree_paths:
            result.extend(["", ".. toctree::", "   :hidden:", ""])
            for toctree_path in sorted(toctree_paths):
                result.append("   {}".format(toctree_path))
        result.extend(["", ".. autosummary::", "   :nosignatures:", ""])
        for documenter in documenters:
            template = "   ~{}"
            if show_full_paths:
                template = "   {}"
            path = documenter.package_path.rpartition(self.package_path + ".")[-1]
            result.append(template.format(path))
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def member_documenters_by_section(self) -> List[Tuple[str, List[MemberDocumenter]]]:
        result: MutableMapping[str, List[MemberDocumenter]] = {}
        for documenter in self.member_documenters:
            result.setdefault(documenter.documentation_section, []).append(documenter)
        for module_documenter in self.module_documenters or []:
            if not module_documenter.is_nominative:
                continue
            documenter = module_documenter.member_documenters[0]
            result.setdefault(documenter.documentation_section, []).append(documenter)
        return sorted(result.items())


class SummarizingRootDocumenter(RootDocumenter):
    """
    A summarizing root documenter.

    Like the :py:class:`~uqbar.apis.SummarizingClassDocumenter` and
    :py:class:`~uqbar.apis.SummarizingModuleDocumenter`, this subclass of
    :py:class:`~uqbar.apis.RootDocumenter` generates root API documentation
    with additional information and organization.

    Each visited module or package receives its own section with members
    organized by their documentation sections and listed in autosummary tables.

    ::

        >>> import uqbar.apis
        >>> documenter = uqbar.apis.SummarizingRootDocumenter(
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
           :hidden:
        <BLANKLINE>
           uqbar/io
           uqbar/strings
        <BLANKLINE>
        .. raw:: html
        <BLANKLINE>
           <hr/>
        <BLANKLINE>
        .. rubric:: :ref:`uqbar.io <uqbar--io>`
           :class: section-header
        <BLANKLINE>
        Tools for IO and file-system manipulation.
        <BLANKLINE>
        .. raw:: html
        <BLANKLINE>
           <hr/>
        <BLANKLINE>
        .. rubric:: Classes
           :class: subsection-header
        <BLANKLINE>
        .. autosummary::
           :nosignatures:
        <BLANKLINE>
           ~uqbar.io.DirectoryChange
           ~uqbar.io.Profiler
           ~uqbar.io.RedirectedStreams
           ~uqbar.io.Timer
        <BLANKLINE>
        .. raw:: html
        <BLANKLINE>
           <hr/>
        <BLANKLINE>
        .. rubric:: Functions
           :class: subsection-header
        <BLANKLINE>
        .. autosummary::
           :nosignatures:
        <BLANKLINE>
           ~uqbar.io.find_common_prefix
           ~uqbar.io.find_executable
           ~uqbar.io.open_path
           ~uqbar.io.relative_to
           ~uqbar.io.walk
           ~uqbar.io.write
        <BLANKLINE>
        .. raw:: html
        <BLANKLINE>
           <hr/>
        <BLANKLINE>
        .. rubric:: :ref:`uqbar.strings <uqbar--strings>`
           :class: section-header
        <BLANKLINE>
        Tools for string manipulation.
        <BLANKLINE>
        .. raw:: html
        <BLANKLINE>
           <hr/>
        <BLANKLINE>
        .. rubric:: Functions
           :class: subsection-header
        <BLANKLINE>
        .. autosummary::
           :nosignatures:
        <BLANKLINE>
           ~uqbar.strings.ansi_escape
           ~uqbar.strings.delimit_words
           ~uqbar.strings.normalize
           ~uqbar.strings.to_dash_case
           ~uqbar.strings.to_snake_case

    :param module_documenters: a list of of documenters for modules and
        packages of the root documenter; these are generated by an
        :py:class:`~uqbar.apis.APIBuilder` instance rather than the module
        documenter directly
    """

    def __str__(self):
        result = [
            self.title,
            "=" * len(self.title),
            "",
            ".. toctree::",
            "   :hidden:",
            "",
        ]
        for documenter in self.module_documenters:
            path = documenter.package_path.replace(".", "/")
            if documenter.is_package:
                path += "/index"
            result.append("   {}".format(path))
        for module_documenter, documenters_by_section in self._recurse(self):
            result.extend(
                [
                    "",
                    ".. raw:: html",
                    "",
                    "   <hr/>",
                    "",
                    ".. rubric:: :ref:`{} <{}>`".format(
                        module_documenter.package_path, module_documenter.reference_name
                    ),
                    "   :class: section-header",
                ]
            )
            summary = self._extract_summary(module_documenter)
            if summary:
                result.extend(["", summary])
            for section_name, documenters in documenters_by_section:
                result.extend(
                    [
                        "",
                        ".. raw:: html",
                        "",
                        "   <hr/>",
                        "",
                        ".. rubric:: {}".format(section_name),
                        "   :class: subsection-header",
                        "",
                        ".. autosummary::",
                        "   :nosignatures:",
                        "",
                    ]
                )
                for documenter in documenters:
                    result.append("   ~{}".format(documenter.package_path))
        return "\n".join(result)

    def _recurse(self, documenter):
        result = []
        if isinstance(documenter, ModuleDocumenter) and not documenter.is_nominative:
            result.append((documenter, documenter.member_documenters_by_section))
        for module_documenter in documenter.module_documenters:
            result.extend(self._recurse(module_documenter))
        return result

    @classmethod
    def _extract_summary(cls, documenter):
        lines = normalize(documenter.client.__doc__ or "").splitlines()
        if not lines:
            return
        settings = mock.Mock(
            auto_id_prefix="",
            id_prefix="",
            language_code="en",
            pep_reference=False,
            rfc_reference=False,
        )
        document = new_document("", settings)
        try:
            summary = extract_summary(lines, document)
        except Exception:
            return ""
        return "\n".join(textwrap.wrap(summary, 79))


class ImmaterialClassDocumenter(SummarizingClassDocumenter):
    """
    Class documenter that plays well with sphinx-immaterial theme.
    """

    ignored_special_methods: Tuple[str, ...] = (
        "__delattr__",
        "__dict__",
        "__eq__",
        "__getattribute__",
        "__getnewargs__",
        "__getstate__",
        "__hash__",
        "__init__",
        "__new__",
        "__postinit__",
        "__reduce__",
        "__reduce_ex__",
        "__repr__",
        "__setattr__",
        "__setstate__",
        "__sizeof__",
        "__str__",
        "__subclasshook__",
        "fromkeys",
        "pipe_cloexec",
    )

    def __str__(self) -> str:
        name = getattr(self.client, "__name__")
        if issubclass(self.client, Exception):  # type: ignore
            return ".. autoexception:: {}".format(name)
        result = [".. autoclass:: {}".format(name), "   :show-inheritance:"]
        if issubclass(self.client, enum.Enum):  # type: ignore
            result.extend(["   :members:", "   :undoc-members:"])
        result.append("")
        for attr in sorted(
            inspect.classify_class_attrs(cast(type, self.client)), key=lambda x: x.name
        ):
            if attr.defining_class is not self.client:
                continue
            if attr.name.startswith("_") and not attr.name.startswith("__"):
                continue
            if attr.name.startswith("__") and attr.name in self.ignored_special_methods:
                continue
            if attr.kind in ("method", "class method", "static method"):
                result.append(f"   .. automethod:: {attr.name}")
            elif attr.kind in ("property"):
                result.append(f"   .. autoproperty:: {attr.name}")
        return "\n".join(result)


class ImmaterialModuleDocumenter(ModuleDocumenter):
    """
    Module documenter that plays well with sphinx-immaterial theme.
    """

    def _build_toc(self, documenters, **kwargs) -> List[str]:
        result: List[str] = []
        if not documenters:
            return result
        result.extend(["", ".. toctree::", "   :hidden:"])
        result.append("")
        module_documenters = [_ for _ in documenters if isinstance(_, type(self))]
        for module_documenter in module_documenters:
            path = self._build_toc_path(module_documenter)
            if path:
                result.append("   {}".format(path))
        return result
