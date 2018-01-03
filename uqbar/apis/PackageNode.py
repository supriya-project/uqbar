import uqbar.containers


class PackageNode(uqbar.containers.UniqueTreeContainer):
    """
    A :py:class:`~uqbar.containers.UniqueTreeContainer` subclass used during
    API construction to proxy packages.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Internals'

    ### INITIALIZER ###

    def __init__(
        self,
        children=None,
        name=None,
        documenter=None,
        source_path=None,
    ):
        super().__init__(children=children, name=name)
        self._source_path = source_path
        self._documenter = documenter

    ### SPECIAL METHODS ###

    def __str__(self):
        result = ['{}/'.format(self.name)]
        for child in self:
            result.extend('    ' + line for line in str(child).splitlines())
        return '\n'.join(result)

    ### PUBLIC PROPERTIES ###

    @property
    def _node_class(self):
        import uqbar.apis
        return (
            uqbar.apis.ModuleNode,
            uqbar.apis.PackageNode,
            )

    @property
    def documenter(self):
        return self._documenter

    @documenter.setter
    def documenter(self, documenter):
        self._documenter = documenter

    @property
    def package_path(self):
        return self._name

    @property
    def source_path(self):
        return self._source_path

    @source_path.setter
    def source_path(self, source_path):
        self._source_path = source_path
