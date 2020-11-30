"""
Uqbar Sphinx styling extension.

- Adds additional information to autodoc entries.
- Adds additional CSS.

Install by adding ``'uqbar.sphinx.style'`` to the ``extensions`` list in your
Sphinx configuration.
"""
import importlib
import inspect
import pathlib
from typing import Any, Dict

from docutils import nodes
from sphinx import addnodes  # type: ignore
from sphinx.locale import _
from sphinx.util import logging

import uqbar.io

logger = logging.getLogger(__name__)


def handle_class(signature_node, module, object_name, cache):
    """
    Styles ``autoclass`` entries.

    Adds ``abstract`` prefix to abstract classes.
    """
    class_ = getattr(module, object_name, None)
    if class_ is None:
        return
    if class_ not in cache:
        cache[class_] = {}
        attributes = inspect.classify_class_attrs(class_)
        for attribute in attributes:
            cache[class_][attribute.name] = attribute
    if inspect.isabstract(class_):
        emphasis = nodes.emphasis("abstract ", "abstract ", classes=["property"])
        signature_node.insert(0, emphasis)


def handle_method(signature_node, module, object_name, cache):
    """
    Styles ``automethod`` entries.

    Adds link to originating class for inherited methods.
    """
    *class_names, attr_name = object_name.split(".")  # Handle nested classes
    class_ = module
    for class_name in class_names:
        class_ = getattr(class_, class_name, None)
        if class_ is None:
            return
    try:
        inspected_attr = cache[class_][attr_name]
        defining_class = inspected_attr.defining_class
    except KeyError:
        # TODO: This is a hack to handle bad interaction between enum and inspect
        defining_class = class_
    if defining_class is not class_:
        reftarget = "{}.{}".format(defining_class.__module__, defining_class.__name__)
        xref_node = addnodes.pending_xref(
            "", refdomain="py", refexplicit=True, reftype="class", reftarget=reftarget
        )
        name_node = nodes.literal(
            "", "{}".format(defining_class.__name__), classes=["descclassname"]
        )
        xref_node.append(name_node)
        desc_annotation = list(signature_node.traverse(addnodes.desc_annotation))
        index = len(desc_annotation)
        class_annotation = addnodes.desc_addname()
        class_annotation.extend([nodes.Text("("), xref_node, nodes.Text(").")])
        class_annotation["xml:space"] = "preserve"
        signature_node.insert(index, class_annotation)
    else:
        is_overridden = False
        for class_ in defining_class.__mro__[1:]:
            if hasattr(class_, attr_name):
                is_overridden = True
        if is_overridden:
            emphasis = nodes.emphasis(
                "overridden ", "overridden ", classes=["property"]
            )
            signature_node.insert(0, emphasis)


def on_doctree_read(app, document):
    """
    Hooks into Sphinx's ``doctree-read`` event.
    """
    cache: Dict[type, Dict[str, object]] = {}
    for desc_node in document.traverse(addnodes.desc):
        if desc_node.get("domain") != "py":
            continue
        signature_node = list(desc_node.traverse(addnodes.desc_signature))[0]
        module_name = signature_node.get("module")
        object_name = signature_node.get("fullname")
        object_type = desc_node.get("objtype")
        module = importlib.import_module(module_name)
        if object_type == "class":
            handle_class(signature_node, module, object_name, cache)
        elif object_type in ("method", "attribute", "staticmethod", "classmethod"):
            handle_method(signature_node, module, object_name, cache)


def on_builder_inited(app):
    """
    Hooks into Sphinx's ``builder-inited`` event.

    Used for copying over CSS files to theme directory.
    """
    local_css_path = pathlib.Path(__file__).parent / "uqbar.css"
    theme_css_path = (
        pathlib.Path(app.srcdir) / app.config.html_static_path[0] / "uqbar.css"
    )
    with local_css_path.open("r") as file_pointer:
        local_css_contents = file_pointer.read()
    uqbar.io.write(local_css_contents, theme_css_path)


# Make definition list terms linkable


def visit_classifier(self, node):
    self.body.append(self.starttag(node, "span", "", CLASS="classifier"))


def depart_classifier(self, node):
    self.body.append("</span>")
    next_node = node.next_node(descend=False, siblings=True)
    if not isinstance(next_node, nodes.classifier):
        self.body.append("</dt>")


def visit_definition(self, node):
    self.body.append(self.starttag(node, "dd", ""))


def depart_definition(self, node):
    self.body.append("</dd>\n")


def visit_term(self, node):
    self.body.append(self.starttag(node, "dt", ""))


def depart_term(self, node):
    next_node = node.next_node(descend=False, siblings=True)
    if isinstance(next_node, nodes.classifier):
        pass
    else:
        self.add_permalink_ref(node, _("Permalink to this term"))
        self.body.append("</dt>")


# Setup


def setup(app) -> Dict[str, Any]:
    """
    Sets up Sphinx extension.
    """
    app.connect("doctree-read", on_doctree_read)
    app.connect("builder-inited", on_builder_inited)
    app.add_css_file("uqbar.css")
    app.add_node(
        nodes.classifier, override=True, html=(visit_classifier, depart_classifier)
    )
    app.add_node(
        nodes.definition, override=True, html=(visit_definition, depart_definition)
    )
    app.add_node(nodes.term, override=True, html=(visit_term, depart_term))
    return {
        "version": uqbar.__version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
