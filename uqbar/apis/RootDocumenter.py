import pathlib


class RootDocumenter:

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Documenters'

    ### INITIALIZER ###

    def __init__(self, module_documenters=None):
        import uqbar.apis
        if module_documenters is not None:
            assert all(isinstance(_, uqbar.apis.ModuleDocumenter)
                for _ in module_documenters), module_documenters
            module_documenters = tuple(module_documenters)
        self._module_documenters = module_documenters or ()

    ### SPECIAL METHODS ###

    def __str__(self):
        result = ['API', '===', '']
        if self.module_documenters:
            result.extend(['.. toctree::', ''])
            for module_documenter in self.module_documenters:
                path = module_documenter.package_path.replace('.', '/')
                if module_documenter.is_package:
                    path = '{}/index'.format(path)
                result.append('   {}'.format(path))
            result.append('')
        return '\n'.join(result)

    ### PUBLIC PROPERTIES ###

    @property
    def documentation_path(self):
        return pathlib.Path('index.rst')

    @property
    def module_documenters(self):
        return self._module_documenters
