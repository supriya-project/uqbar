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
import importlib
import pathlib
import sphinx
import types
import uqbar.apis


def on_builder_inited(app: sphinx.application.Sphinx):
    """
    Hooks into Sphinx's ``builder-inited`` event.

    Builds out the ReST API source.
    """
    config = app.builder.config

    target_directory = (
        pathlib.Path(app.builder.env.srcdir) /
        config.uqbar_api_directory_name
        )

    initial_source_paths = []
    source_paths = config.uqbar_api_source_paths
    for source_path in source_paths:
        if isinstance(source_path, types.ModuleType):
            if hasattr(source_path, '__path__'):
                initial_source_paths.extend(source_path.__path__)
            else:
                initial_source_paths.extend(source_path.__file__)
            continue
        try:
            module = importlib.import_module(source_path)
            if hasattr(module, '__path__'):
                initial_source_paths.extend(module.__path__)
            else:
                initial_source_paths.append(module.__file__)
        except ImportError:
            initial_source_paths.append(source_path)

    api_builder = uqbar.apis.APIBuilder(
        initial_source_paths=initial_source_paths,
        target_directory=target_directory,
        document_private_members=config.uqbar_api_document_private_members,
        document_private_modules=config.uqbar_api_document_private_modules,
        member_documenter_classes=config.uqbar_api_member_documenter_classes,
        module_documenter_class=config.uqbar_api_module_documenter_class,
        root_documenter_class=config.uqbar_api_root_documenter_class,
        title=config.uqbar_api_title,
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
