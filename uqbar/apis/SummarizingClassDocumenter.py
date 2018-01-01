import inspect
import typing
from uqbar.apis.ClassDocumenter import ClassDocumenter


class SummarizingClassDocumenter(ClassDocumenter):

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
            inherited_attributes,
            methods,
            readonly_properties,
            readwrite_properties,
            special_methods,
            static_methods,
            ) = self._classify_class_attributes()
        result = [
            '.. autoclass:: {}'.format(self.client.__name__),
            '   :show-inheritance:',
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
        ) -> typing.Sequence[str]:
        result = []
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
                directive, self.client.__name__, attribute.name)
            if self.client is not attribute.defining_class:
                result.extend([
                    '   .. container:: inherited',
                    '',
                    '   {}'.format(autodoc_directive),
                    ])
            else:
                result.append(autodoc_directive)
        return result

    def _classify_class_attributes(self):
        class_methods = []
        data = []
        inherited_attributes = []
        methods = []
        readonly_properties = []
        readwrite_properties = []
        special_methods = []
        static_methods = []
        attrs = inspect.classify_class_attrs(self.client)
        for attr in attrs:
            if attr.defining_class is object:
                continue
            if attr.defining_class is not self.client:
                inherited_attributes.append(attr)
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
        inherited_attributes = tuple(sorted(inherited_attributes))
        methods = tuple(sorted(methods))
        readonly_properties = tuple(sorted(readonly_properties))
        readwrite_properties = tuple(sorted(readwrite_properties))
        special_methods = tuple(sorted(special_methods))
        static_methods = tuple(sorted(static_methods))
        result = (
            class_methods,
            data,
            inherited_attributes,
            methods,
            readonly_properties,
            readwrite_properties,
            special_methods,
            static_methods,
            )
        return result
