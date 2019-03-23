import importlib
from typing import Any, Dict, List  # noqa

from sphinx.util import logging
from sphinx.util.console import bold

import uqbar.book.sphinx
from uqbar.book.console import ConsoleError
from uqbar.book.extensions import GrapherExtension

logger = logging.getLogger(__name__)


def on_builder_inited(app):
    app.cache_db_path = ":memory:"
    if app.config["uqbar_book_use_cache"]:
        logger.info(bold("[uqbar-book]"), nonl=True)
        logger.info(" initializing cache db")
        app.connection = uqbar.book.sphinx.create_cache_db(app.cache_db_path)


def on_config_inited(app, config):
    for extension_path in config["uqbar_book_extensions"] or (
        "uqbar.book.extensions.GrapherExtension",
    ):
        extension_module_path, _, extension_class_name = extension_path.rpartition(".")
        extension_module = importlib.import_module(extension_module_path)
        extension_class = getattr(extension_module, extension_class_name)
        extension_class.setup_sphinx(app)


def on_doctree_read(app, document):
    extensions = [GrapherExtension()]
    literal_blocks = uqbar.book.sphinx.collect_literal_blocks(document)
    cache_mapping = uqbar.book.sphinx.group_literal_blocks_by_cache_path(literal_blocks)
    node_mapping = {}
    use_cache = bool(app.config["uqbar_book_use_cache"])
    for cache_path, literal_block_groups in cache_mapping.items():
        kwargs = dict(
            extensions=extensions,
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
    app.add_config_value("uqbar_book_console_setup", [], "env")
    app.add_config_value("uqbar_book_console_teardown", [], "env")
    app.add_config_value("uqbar_book_extensions", [], "env")
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
