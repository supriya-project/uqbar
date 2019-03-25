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

from sphinx.util import logging
from sphinx.util.console import bold

import uqbar.book.sphinx
from uqbar.book.console import ConsoleError

logger = logging.getLogger(__name__)


def on_builder_inited(app):
    """
    Hooks into Sphinx's ``builder-inited`` event.
    """
    app.cache_db_path = ":memory:"
    if app.config["uqbar_book_use_cache"]:
        logger.info(bold("[uqbar-book]"), nonl=True)
        logger.info(" initializing cache db")
        app.connection = uqbar.book.sphinx.create_cache_db(app.cache_db_path)


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


def on_doctree_read(app, document):
    """
    Hooks into Sphinx's ``doctree-read`` event.
    """
    literal_blocks = uqbar.book.sphinx.collect_literal_blocks(document)
    cache_mapping = uqbar.book.sphinx.group_literal_blocks_by_cache_path(literal_blocks)
    node_mapping = {}
    use_cache = bool(app.config["uqbar_book_use_cache"])
    for cache_path, literal_block_groups in cache_mapping.items():
        kwargs = dict(
            extensions=app.uqbar_book_extensions,
            setup_lines=app.config["uqbar_book_console_setup"],
            teardown_lines=app.config["uqbar_book_console_teardown"],
            use_black=bool(app.config["uqbar_book_use_black"]),
        )
        for literal_blocks in literal_block_groups:
            try:
                if use_cache:
                    local_node_mapping = uqbar.book.sphinx.interpret_code_blocks_with_cache(
                        literal_blocks, cache_path, app.connection, **kwargs
                    )
                else:
                    local_node_mapping = uqbar.book.sphinx.interpret_code_blocks(
                        literal_blocks, **kwargs
                    )
                node_mapping.update(local_node_mapping)
            except ConsoleError as exception:
                message = exception.args[0].splitlines()[-1]
                logger.warning(message, location=exception.args[1])
                if app.config["uqbar_book_strict"]:
                    raise
    uqbar.book.sphinx.rebuild_document(document, node_mapping)


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
    app.connect("builder-inited", on_builder_inited)
    app.connect("config-inited", on_config_inited)
    app.connect("doctree-read", on_doctree_read)
    app.connect("build-finished", on_build_finished)
    return {
        "version": uqbar.__version__,
        "parallel_read_safe": False,
        "parallel_write_safe": True,
    }
