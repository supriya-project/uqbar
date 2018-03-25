import inspect
from typing import List
from uqbar.apis.ClassDocumenter import ClassDocumenter


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
        >>> path = 'uqbar.apis.SummarizingClassDocumenter.SummarizingClassDocumenter'
        >>> documenter = uqbar.apis.SummarizingClassDocumenter(path)
        >>> documentation = str(documenter)
        >>> print(documentation)
        .. autoclass:: SummarizingClassDocumenter
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
           .. automethod:: SummarizingClassDocumenter.validate_client
        <BLANKLINE>
           .. raw:: html
        <BLANKLINE>
              <hr/>
        <BLANKLINE>
           .. rubric:: Read-only properties
              :class: class-header
        <BLANKLINE>
           .. autoattribute:: SummarizingClassDocumenter.client
        <BLANKLINE>
           .. autoattribute:: SummarizingClassDocumenter.documentation_section
        <BLANKLINE>
           .. autoattribute:: SummarizingClassDocumenter.package_path

    :param package_path: the module path and name of the member to document
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Documenters'

    ignored_special_methods = (
        '__dict__',
        '__getattribute__',
        '__getnewargs__',
        '__getstate__',
        '__init__',
        '__reduce__',
        '__reduce_ex__',
        '__setstate__',
        '__sizeof__',
        '__subclasshook__',
        'fromkeys',
        'pipe_cloexec',
        )

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        (
            class_methods,
            data,
            methods,
            readonly_properties,
            readwrite_properties,
            special_methods,
            static_methods,
            ) = self._classify_class_attributes()
        result = [
            '.. autoclass:: {}'.format(getattr(self.client, '__name__')),
            ]
        result.extend(self._build_attribute_section(
            special_methods,
            'automethod',
            'Special methods',
            ))
        result.extend(self._build_attribute_section(
            methods,
            'automethod',
            'Methods',
            ))
        result.extend(self._build_attribute_section(
            sorted(class_methods + static_methods, key=lambda x: x.name),
            'automethod',
            'Class & static methods',
            ))
        result.extend(self._build_attribute_section(
            readwrite_properties,
            'autoattribute',
            'Read/write properties',
            ))
        result.extend(self._build_attribute_section(
            readonly_properties,
            'autoattribute',
            'Read-only properties',
            ))
        return '\n'.join(result)

    ### PRIVATE METHODS ###

    def _build_attribute_section(
        self,
        attributes,
        directive: str,
        title: str,
        ) -> List[str]:
        result: List[str] = []
        if not attributes:
            return result
        result.extend([
            '',
            '   .. raw:: html',
            '',
            '      <hr/>',
            '',
            '   .. rubric:: {}'.format(title),
            '      :class: class-header',
            ])
        for attribute in attributes:
            result.append('')
            autodoc_directive = '   .. {}:: {}.{}'.format(
                directive, getattr(self.client, '__name__'), attribute.name)
            result.append(autodoc_directive)
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
                getattr(self.client, '__documentation_ignore_inherited__', None) and
                attr.defining_class is not self.client
                ):
                continue
            if attr.kind == 'method':
                if attr.name not in self.ignored_special_methods:
                    if attr.name.startswith('__'):
                        special_methods.append(attr)
                    elif not attr.name.startswith('_'):
                        methods.append(attr)
            elif attr.kind == 'class method':
                if attr.name not in self.ignored_special_methods:
                    if attr.name.startswith('__'):
                        special_methods.append(attr)
                    elif not attr.name.startswith('_'):
                        class_methods.append(attr)
            elif attr.kind == 'static method':
                if attr.name not in self.ignored_special_methods:
                    if attr.name.startswith('__'):
                        special_methods.append(attr)
                    elif not attr.name.startswith('_'):
                        static_methods.append(attr)
            elif attr.kind == 'property' and not attr.name.startswith('_'):
                if attr.object.fset is None:
                    readonly_properties.append(attr)
                else:
                    readwrite_properties.append(attr)
            elif attr.kind == 'data' and not attr.name.startswith('_') \
                and attr.name not in getattr(self.client, '__slots__', ()):
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
