"""
Uqbar Sphinx API generation extension.

Install by adding ``'uqbar.sphinx.api'`` to the ``extensions`` list in your
Sphinx configuration.

This extension provides the following configuration values which correspond to
the initialization arguments to the :py:class:`uqbar.apis.APIBuilder` class.

- ``uqbar_api_directory_name``
- ``uqbar_api_document_private_members``
- ``uqbar_api_document_private_modules``
- ``uqbar_api_member_documenter_classes``
- ``uqbar_api_module_documenter_class``
- ``uqbar_api_root_documenter_class``
- ``uqbar_api_source_paths``
- ``uqbar_api_title``

"""
import sphinx
import uqbar.apis


def on_builder_inited(app: sphinx.application.Sphinx):
    """
    Hooks into Sphinx's ``builder-inited`` event.

    Builds out the ReST API source.
    """
    api_builder = uqbar.apis.APIBuilder(
        initial_source_paths=app.config,
        target_directory=app.config,
        document_private_members=app.config,
        document_private_modules=app.config,
        member_documenter_classes=app.config,
        module_documenter_class=app.config,
        root_documenter_class=app.config,
        )
    api_builder()


def setup(app: sphinx.application.Sphinx):
    """
    Sets up Sphinx extension.
    """
    app.connect('builder-inited', on_builder_inited)
    app.add_config_value('uqbar_api_directory_name', 'api', 'env')
    app.add_config_value('uqbar_api_document_private_members', False, 'env')
    app.add_config_value('uqbar_api_document_private_modules', False, 'env')
    app.add_config_value('uqbar_api_member_documenter_classes', None, 'env')
    app.add_config_value('uqbar_api_module_documenter_class', None, 'env')
    app.add_config_value('uqbar_api_root_documenter_class', None, 'env')
    app.add_config_value('uqbar_api_source_paths', [], 'env')
    app.add_config_value('uqbar_api_title', 'API', 'env')
