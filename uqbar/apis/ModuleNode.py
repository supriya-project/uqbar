import uqbar.containers


class ModuleNode(uqbar.containers.UniqueTreeNode):
    """
    A :py:class:`~uqbar.containers.UniqueTreeNode` subclass used during API
    construction to proxy modules.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Internals"

    ### INITIALIZER ###

    def __init__(self, name=None, documenter=None, source_path=None):
        super().__init__(name=name)
        self._documenter = documenter
        self._source_path = source_path

    ### SPECIAL METHODS ###

    def __str__(self):
        return "{}".format(self.name)

    ### PUBLIC PROPERTIES ###

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
