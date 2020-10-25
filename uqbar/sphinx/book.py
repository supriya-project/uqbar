"""
Uqbar Sphinx executable examples extension.

Runs every Python-formatted literal block through a console, and captures
output. Can be extended to capture non-terminal output like Graphviz graphs,
other images, audio, etc. via an extension system.

The extension groups all top-level literal blocks in a document into a suite to
be executed consecutively in a console. All literal blocks in each class,
method and function docstring are grouped and executed separately in isolated
namespaces. When ``uqbar_book_use_cache`` is ``True``, the docstring grouping
allows inherited docstring suites to be executed only once per Sphinx build.

Install by adding ``'uqbar.sphinx.book'`` to the ``extensions`` list in your
Sphinx configuration.

This extension provides the following configuration values:

``uqbar_book_console_setup``:
    list of strings to run in the console before executing a suite of literal
    blocks, e.g. ``["import uqbar"]``

``uqbar_book_console_teardown``:
    list of strings to run in the console after executing a suite of literal
    blocks, even if execution halts due to error, e.g.
    ``["important_thing.shutdown()", "other_thing.cleanup()"]``

``uqbar_book_extensions``:
    list of class paths to extensions, e.g.
    ``["uqbar.book.extensions.GraphExtension"]``

``uqbar_book_strict``:
    whether to fail the Sphinx build on encountering an unexpected error

``uqbar_book_use_black``:
    whether to use ``black`` to format console input

``uqbar_book_use_cache``:
    whether to use a caching system to avoid re-executing identical literal
    block suites

"""
import importlib
from typing import Any, Dict

from docutils.nodes import SkipNode
from sphinx.util import logging
from sphinx.util.console import bold  # type: ignore

import uqbar
from uqbar.book.console import ConsoleError
from uqbar.book.sphinx import (
    UqbarBookDefaultsDirective,
    UqbarBookDirective,
    UqbarBookImportDirective,
    collect_literal_blocks,
    console_context,
    create_cache_db,
    group_literal_blocks_by_cache_path,
    interpret_code_blocks,
    interpret_code_blocks_with_cache,
    rebuild_document,
    uqbar_book_defaults_block,
    uqbar_book_import_block,
)

logger = logging.getLogger(__name__)


def on_builder_inited(app):
    """
    Hooks into Sphinx's ``builder-inited`` event.
    """
    app.cache_db_path = ":memory:"
    if app.config["uqbar_book_use_cache"]:
        logger.info(bold("[uqbar-book]"), nonl=True)
        logger.info(" initializing cache db")
        app.connection = create_cache_db(app.cache_db_path)


def on_config_inited(app, config):
    """
    Hooks into Sphinx's ``config-inited`` event.
    """
    extension_paths = config["uqbar_book_extensions"] or [
        "uqbar.book.extensions.GraphExtension"
    ]
    app.uqbar_book_extensions = []
    for extension_path in extension_paths:
        module_name, _, class_name = extension_path.rpartition(".")
        module = importlib.import_module(module_name)
        extension_class = getattr(module, class_name)
        extension_class.setup_sphinx(app)
        app.uqbar_book_extensions.append(extension_class)
    # Verify early that any setup / teardown works
    try:
        with console_context(
            extensions=app.uqbar_book_extensions,
            setup_lines=config["uqbar_book_console_setup"],
            teardown_lines=config["uqbar_book_console_teardown"],
        ):
            pass
    except ConsoleError:
        logger.error("uqbar.sphinx.book console setup/teardown failed")
        raise


def on_doctree_read(app, document):
    """
    Hooks into Sphinx's ``doctree-read`` event.
    """
    literal_blocks = collect_literal_blocks(document)
    cache_mapping = group_literal_blocks_by_cache_path(literal_blocks)
    node_mapping = {}
    use_cache = bool(app.config["uqbar_book_use_cache"])
    kwargs = dict(
        document=document,
        extensions=app.uqbar_book_extensions,
        setup_lines=app.config["uqbar_book_console_setup"],
        teardown_lines=app.config["uqbar_book_console_teardown"],
        use_black=bool(app.config["uqbar_book_use_black"]),
    )
    for cache_path, literal_block_groups in cache_mapping.items():
        for literal_blocks in literal_block_groups:
            try:
                if use_cache:
                    local_node_mapping = interpret_code_blocks_with_cache(
                        literal_blocks, cache_path, app.connection, **kwargs
                    )
                else:
                    local_node_mapping = interpret_code_blocks(literal_blocks, **kwargs)
                node_mapping.update(local_node_mapping)
            except ConsoleError as exception:
                # message = exception.args[0].splitlines()[-1]
                # logger.warning(message, location=exception.args[1])
                message = "\n    " + "\n    ".join(
                    line.rstrip() for line in exception.args[0].rstrip().splitlines()
                )
                logger.warning(message, location=exception.args[1])
                if app.config["uqbar_book_strict"]:
                    raise
    rebuild_document(document, node_mapping)


def on_build_finished(app, exception):
    """
    Hooks into Sphinx's ``build-finished`` event.
    """
    if not app.config["uqbar_book_use_cache"]:
        return
    logger.info("")
    for row in app.connection.execute("SELECT path, hits FROM cache ORDER BY path"):
        path, hits = row
        if not hits:
            continue
        logger.info(bold("[uqbar-book]"), nonl=True)
        logger.info(" Cache hits for {}: {}".format(path, hits))


def skip_node(self, node):
    raise SkipNode


def setup(app) -> Dict[str, Any]:
    """
    Sets up Sphinx extension.
    """
    app.add_config_value("uqbar_book_console_setup", [], "env")
    app.add_config_value("uqbar_book_console_teardown", [], "env")
    app.add_config_value(
        "uqbar_book_extensions", ["uqbar.book.extensions.GraphExtension"], "env"
    )
    app.add_config_value("uqbar_book_strict", False, "env")
    app.add_config_value("uqbar_book_use_black", False, "env")
    app.add_config_value("uqbar_book_use_cache", True, "env")
    app.add_config_value("uqbar_book_block_options", {}, "env")
    app.add_directive("book", UqbarBookDirective)
    app.add_directive("book-defaults", UqbarBookDefaultsDirective)
    app.add_directive("book-import", UqbarBookImportDirective)

    for node_class in [uqbar_book_defaults_block, uqbar_book_import_block]:
        app.add_node(
            node_class,
            html=[skip_node, None],
            latex=[skip_node, None],
            text=[skip_node, None],
        )
    app.connect("builder-inited", on_builder_inited)
    app.connect("config-inited", on_config_inited)
    app.connect("doctree-read", on_doctree_read)
    app.connect("build-finished", on_build_finished)
    return {
        "version": uqbar.__version__,
        "parallel_read_safe": False,
        "parallel_write_safe": True,
    }
