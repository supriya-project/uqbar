import types
from uqbar.apis.MemberDocumenter import MemberDocumenter


class FunctionDocumenter(MemberDocumenter):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Documenters'

    ### SPECIAL METHODS ###

    def __str__(self):
        return '.. autofunction:: {}'.format(
            self.client.__name__,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def validate_client(cls, client, module_path):
        return (
            isinstance(client, types.FunctionType) and
            client.__module__ == module_path
            )

    ### PUBLIC PROPERTIES ###

    @property
    def documentation_section(self):
        return 'Functions'
