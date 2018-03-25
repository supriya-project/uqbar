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
import sphinx  # type:ignore
import uqbar.io
from docutils import nodes
from sphinx import addnodes  # type: ignore
from typing import Dict


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
        labelnode = addnodes.only(expr='html')
        labelnode.append(nodes.emphasis(
            'abstract ',
            'abstract ',
            classes=['property'],
            ))
        signature_node.insert(0, labelnode)


def handle_method(signature_node, module, object_name, cache):
    """
    Styles ``automethod`` entries.

    Adds ``abstract`` prefix to abstract methods.

    Adds link to originating class for inherited methods.
    """
    cls_name, attr_name = object_name.split('.')
    class_ = getattr(module, cls_name, None)
    if class_ is None:
        return
    attr = getattr(class_, attr_name)
    inspected_attr = cache[class_][attr_name]
    label_node = addnodes.only(expr='html')
    defining_class = inspected_attr.defining_class
    if defining_class is not class_:
        reftarget = '{}.{}'.format(
            defining_class.__module__,
            defining_class.__name__,
            )
        xref_node = addnodes.pending_xref(
            '',
            refdomain='py',
            refexplicit=True,
            reftype='class',
            reftarget=reftarget,
            )
        xref_node.append(nodes.literal(
            '',
            '{}'.format(defining_class.__name__),
            classes=['descclassname'],
            ))
        html_only_class_name_node = addnodes.only(expr='html')
        html_only_class_name_node.append(nodes.Text('('))
        html_only_class_name_node.append(xref_node)
        html_only_class_name_node.append(nodes.Text(').'))
        latex_only_class_name_node = addnodes.only(expr='latex')
        latex_only_class_name_node.append(nodes.Text(
            '({}).'.format(defining_class.__name__),
            ))
        signature_node.insert(0, html_only_class_name_node)
        signature_node.insert(0, latex_only_class_name_node)
    if getattr(attr, '__isabstractmethod__', False):
        label_node.append(nodes.emphasis(
            'abstract ',
            'abstract ',
            classes=['property'],
            ))
        signature_node.insert(0, label_node)


def on_doctree_read(
    app: sphinx.application.Sphinx,
    document,
    ):
    """
    Hooks into Sphinx's ``doctree-read`` event.
    """
    cache: Dict[type, Dict[str, object]] = {}
    for desc_node in document.traverse(addnodes.desc):
        if desc_node.get('domain') != 'py':
            continue
        signature_node = desc_node.traverse(addnodes.desc_signature)[0]
        module_name = signature_node.get('module')
        object_name = signature_node.get('fullname')
        object_type = desc_node.get('objtype')
        module = importlib.import_module(module_name)
        if object_type == 'class':
            handle_class(signature_node, module, object_name, cache)
        elif object_type in (
            'method',
            'attribute',
            'staticmethod', 'classmethod'
            ):
            handle_method(signature_node, module, object_name, cache)


def on_builder_inited(app: sphinx.application.Sphinx):
    """
    Hooks into Sphinx's ``builder-inited`` event.

    Used for copying over CSS files to theme directory.
    """
    local_css_path = pathlib.Path(__file__).parent / 'uqbar.css'
    theme_css_path = (
        pathlib.Path(app.srcdir) /
        app.config.html_static_path[0] /
        'uqbar.css'
        )
    with local_css_path.open('r') as file_pointer:
        local_css_contents = file_pointer.read()
    uqbar.io.write(local_css_contents, theme_css_path)


def setup(app: sphinx.application.Sphinx):
    """
    Sets up Sphinx extension.
    """
    app.connect('doctree-read', on_doctree_read)
    app.connect('builder-inited', on_builder_inited)
    app.add_stylesheet('uqbar.css')
