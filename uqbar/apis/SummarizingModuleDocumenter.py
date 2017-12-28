from uqbar.apis.ModuleDocumenter import ModuleDocumenter


class SummarizingModuleDocumenter(ModuleDocumenter):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Documenters'

    ### SPECIAL METHODS ###

    def __str__(self):
        result = self.build_preamble()
        if self.is_nominative:
            result.extend(['', str(self.member_documenters[0])])
        else:
            if self.is_package:
                subpackage_documenters = [
                    _ for _ in self.module_documenters or []
                    if _.is_package or not _.is_nominative
                    ]
                if subpackage_documenters:
                    result.extend([
                        '',
                        '.. raw:: html',
                        '',
                        '   <hr/>',
                        '',
                        '.. rubric:: Subpackages',
                        '   :class: section-header',
                        ])
                    result.extend(self.build_toc(
                        subpackage_documenters,
                        show_full_paths=True,
                        ))
            for section, documenters in self.member_documenters_by_section:
                result.extend([
                    '',
                    '.. raw:: html',
                    '',
                    '   <hr/>',
                    '',
                    '.. rubric:: {}'.format(section),
                    '   :class: section-header',
                    ])
                local_documenters = [
                    documenter for documenter in documenters
                    if documenter.client.__module__ == self.package_path
                    ]
                if local_documenters != documenters:
                    result.extend(self.build_toc(documenters))
                for local_documenter in local_documenters:
                    result.extend(['', str(local_documenter)])
        return '\n'.join(result)

    ### PUBLIC METHODS ###

    def build_toc(self, documenters, show_full_paths=False):
        result = []
        if not documenters:
            return result
        result.extend(['', '.. toctree::', '   :hidden:', ''])
        toctree_paths = set()
        for documenter in documenters:
            path = documenter.package_path.partition(
                self.package_path)[-1]
            if not isinstance(documenter, ModuleDocumenter):
                path = path.rpartition('.')[0]
            elif documenter.is_package:
                path += '/index'
            if path.startswith('.'):
                path = path[1:]
            if path:
                toctree_paths.add(path)
        for toctree_path in sorted(toctree_paths):
            result.append('   {}'.format(toctree_path))
        result.extend([
            '',
            '.. autosummary::',
            '   :nosignatures:',
            '',
            ])
        for documenter in documenters:
            template = '   ~{}'
            if show_full_paths:
                template = '   {}'
            result.append(template.format(documenter.package_path))
        return result

    @property
    def member_documenters_by_section(self):
        result = {}
        for documenter in self.member_documenters:
            result.setdefault(
                documenter.documentation_section, []).append(documenter)
        for module_documenter in self.module_documenters or []:
            if not module_documenter.is_nominative:
                continue
            documenter = module_documenter.member_documenters[0]
            result.setdefault(
                documenter.documentation_section, []).append(documenter)
        return sorted(result.items())
