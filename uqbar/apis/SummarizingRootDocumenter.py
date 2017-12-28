from uqbar.apis.ModuleDocumenter import ModuleDocumenter
from uqbar.apis.RootDocumenter import RootDocumenter


class SummarizingRootDocumenter(RootDocumenter):

    def __str__(self):
        result = [
            'API',
            '===',
            '',
            '.. toctree::',
            '   :hidden:',
            '',
            ]
        for documenter in self.module_documenters:
            path = documenter.package_path.replace('.', '/')
            if documenter.is_package:
                path += '/index'
            result.append('   {}'.format(path))
        for module_documenter, documenters_by_section in self._recurse(self):
            result.extend([
                '',
                '.. raw:: html',
                '',
                '   <hr/>',
                '',
                '.. rubric:: :ref:`{} <{}>`'.format(
                    module_documenter.package_path,
                    module_documenter.reference_name,
                    ),
                '   :class: section-header',
                ])
            for section_name, documenters in documenters_by_section:
                result.extend([
                    '',
                    '-  {}'.format(section_name),
                    '',
                    '   .. autosummary::',
                    '      :nosignatures:',
                    '',
                    ])
                for documenter in documenters:
                    result.append('      ~{}'.format(documenter.package_path))
        return '\n'.join(result)

    def _recurse(self, documenter):
        result = []
        if (
            isinstance(documenter, ModuleDocumenter) and
            not documenter.is_nominative
            ):
            result.append((
                documenter,
                documenter.member_documenters_by_section,
                ))
        for module_documenter in documenter.module_documenters:
            result.extend(self._recurse(module_documenter))
        return result
