"""
Uqbar Sphinx API generation extension.

Install by adding ``'uqbar.sphinx.api'`` to the ``extensions`` list in your
Sphinx configuration.

This extension provides the following configuration values which correspond to
the initialization arguments to the :py:class:`uqbar.apis.APIBuilder` class.

- ``uqbar_api_directory_name`` (default: ``api``)
- ``uqbar_api_document_empty_modules`` (default: ``False``)
- ``uqbar_api_document_private_members`` (default: ``False``)
- ``uqbar_api_document_private_modules`` (default: ``False``)
- ``uqbar_api_member_documenter_classes`` (default: ``None``)
- ``uqbar_api_module_documenter_class`` (default: ``None``)
- ``uqbar_api_root_documenter_class`` (default: ``None``)
- ``uqbar_api_source_paths`` (default: ``[]``)
- ``uqbar_api_title`` (default: ``API``)

reStructuredText source files will be generated for the modules given by
``uqbar_api_source_paths`` in the directory ``uqbar_api_directory_name``
relative to your Sphinx source directory.
"""
import importlib
import pathlib
import sphinx.application  # type: ignore
import types
import uqbar.apis
from typing import List  # noqa


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

    initial_source_paths: List[str] = []
    source_paths = config.uqbar_api_source_paths
    for source_path in source_paths:
        if isinstance(source_path, types.ModuleType):
            if hasattr(source_path, '__path__'):
                initial_source_paths.extend(getattr(source_path, '__path__'))
            else:
                initial_source_paths.extend(source_path.__file__)
            continue
        try:
            module = importlib.import_module(source_path)
            if hasattr(module, '__path__'):
                initial_source_paths.extend(getattr(module, '__path__'))
            else:
                initial_source_paths.append(module.__file__)
        except ImportError:
            initial_source_paths.append(source_path)

    root_documenter_class = config.uqbar_api_root_documenter_class
    if isinstance(root_documenter_class, str):
        module_name, _, class_name = root_documenter_class.rpartition('.')
        module = importlib.import_module(module_name)
        root_documenter_class = getattr(module, class_name)

    module_documenter_class = config.uqbar_api_module_documenter_class
    if isinstance(module_documenter_class, str):
        module_name, _, class_name = module_documenter_class.rpartition('.')
        module = importlib.import_module(module_name)
        module_documenter_class = getattr(module, class_name)

    member_documenter_classes = config.uqbar_api_member_documenter_classes or []
    for i, member_documenter_class in enumerate(member_documenter_classes):
        if isinstance(member_documenter_class, str):
            module_name, _, class_name = member_documenter_class.rpartition('.')
            module = importlib.import_module(module_name)
            member_documenter_classes[i] = getattr(module, class_name)
    if not member_documenter_classes:
        member_documenter_classes = None

    api_builder = uqbar.apis.APIBuilder(
        initial_source_paths=initial_source_paths,
        target_directory=target_directory,
        document_empty_modules=config.uqbar_api_document_empty_modules,
        document_private_members=config.uqbar_api_document_private_members,
        document_private_modules=config.uqbar_api_document_private_modules,
        member_documenter_classes=member_documenter_classes,
        module_documenter_class=module_documenter_class,
        root_documenter_class=root_documenter_class,
        title=config.uqbar_api_title,
        )
    api_builder()


def setup(app: sphinx.application.Sphinx):
    """
    Sets up Sphinx extension.
    """
    app.connect('builder-inited', on_builder_inited)
    app.add_config_value('uqbar_api_directory_name', 'api', 'env')
    app.add_config_value('uqbar_api_document_empty_modules', False, 'env')
    app.add_config_value('uqbar_api_document_private_members', False, 'env')
    app.add_config_value('uqbar_api_document_private_modules', False, 'env')
    app.add_config_value('uqbar_api_member_documenter_classes', None, 'env')
    app.add_config_value('uqbar_api_module_documenter_class', None, 'env')
    app.add_config_value('uqbar_api_root_documenter_class', None, 'env')
    app.add_config_value('uqbar_api_source_paths', [], 'env')
    app.add_config_value('uqbar_api_title', 'API', 'env')
