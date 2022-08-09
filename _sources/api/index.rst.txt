Uqbar API
=========

.. toctree::
   :hidden:

   uqbar/index

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar <uqbar>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.apis <uqbar--apis>`
   :class: section-header

Tools for auto-generating API documention.

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.apis.collect_source_paths
   ~uqbar.apis.source_path_to_package_path

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.apis.builders <uqbar--apis--builders>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.apis.builders.APIBuilder

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.apis.documenters <uqbar--apis--documenters>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.apis.documenters.MemberDocumenter

.. raw:: html

   <hr/>

.. rubric:: Documenters
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.apis.documenters.ClassDocumenter
   ~uqbar.apis.documenters.FunctionDocumenter
   ~uqbar.apis.documenters.ModuleDocumenter
   ~uqbar.apis.documenters.RootDocumenter

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.apis.dummy <uqbar--apis--dummy>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.apis.dummy.MyChildClass
   ~uqbar.apis.dummy.MyParentClass

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.apis.graphs <uqbar--apis--graphs>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.apis.graphs.InheritanceGraph

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.apis.nodes <uqbar--apis--nodes>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Internals
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.apis.nodes.ModuleNode
   ~uqbar.apis.nodes.PackageNode

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.apis.summarizers <uqbar--apis--summarizers>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Documenters
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.apis.summarizers.ImmaterialClassDocumenter
   ~uqbar.apis.summarizers.ImmaterialModuleDocumenter
   ~uqbar.apis.summarizers.SummarizingClassDocumenter
   ~uqbar.apis.summarizers.SummarizingModuleDocumenter
   ~uqbar.apis.summarizers.SummarizingRootDocumenter

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.book <uqbar--book>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.book.console <uqbar--book--console>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.book.console.Console
   ~uqbar.book.console.ConsoleInput
   ~uqbar.book.console.ConsoleOutput
   ~uqbar.book.console.MonkeyPatch

.. raw:: html

   <hr/>

.. rubric:: Exceptions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.book.console.ConsoleError

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.book.extensions <uqbar--book--extensions>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.book.extensions.Extension
   ~uqbar.book.extensions.GraphExtension

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.book.sphinx <uqbar--book--sphinx>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.book.sphinx.UqbarBookDefaultsDirective
   ~uqbar.book.sphinx.UqbarBookDirective
   ~uqbar.book.sphinx.UqbarBookImportDirective
   ~uqbar.book.sphinx.uqbar_book_defaults_block
   ~uqbar.book.sphinx.uqbar_book_import_block

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.book.sphinx.black_format
   ~uqbar.book.sphinx.collect_literal_blocks
   ~uqbar.book.sphinx.console_context
   ~uqbar.book.sphinx.create_cache_db
   ~uqbar.book.sphinx.find_traceback
   ~uqbar.book.sphinx.group_literal_blocks_by_cache_path
   ~uqbar.book.sphinx.interpret_code_blocks
   ~uqbar.book.sphinx.interpret_code_blocks_with_cache
   ~uqbar.book.sphinx.interpret_import_block
   ~uqbar.book.sphinx.interpret_literal_block
   ~uqbar.book.sphinx.literal_block_to_cache_path
   ~uqbar.book.sphinx.parse_rst
   ~uqbar.book.sphinx.query_cache_db
   ~uqbar.book.sphinx.rebuild_document
   ~uqbar.book.sphinx.update_cache_db

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.containers <uqbar--containers>`
   :class: section-header

Specialized container classes.

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.containers.dependency_graph <uqbar--containers--dependency-graph>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.containers.dependency_graph.DependencyGraph

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.containers.unique_tree <uqbar--containers--unique-tree>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.containers.unique_tree.UniqueTreeContainer
   ~uqbar.containers.unique_tree.UniqueTreeDict
   ~uqbar.containers.unique_tree.UniqueTreeList
   ~uqbar.containers.unique_tree.UniqueTreeNode
   ~uqbar.containers.unique_tree.UniqueTreeSet
   ~uqbar.containers.unique_tree.UniqueTreeTuple

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.enums <uqbar--enums>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Enumerations
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.enums.IntEnumeration
   ~uqbar.enums.StrictEnumeration

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.enums.from_expr

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.ext <uqbar--ext>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.ext.ipython <uqbar--ext--ipython>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.ext.ipython.load_ipython_extension
   ~uqbar.ext.ipython.patch_grapher

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.graphs <uqbar--graphs>`
   :class: section-header

Tools for building Graphviz graphs.

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.graphs.attrs <uqbar--graphs--attrs>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Core Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.graphs.attrs.Attributes

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.graphs.core <uqbar--graphs--core>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Core Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.graphs.core.Edge
   ~uqbar.graphs.core.Graph
   ~uqbar.graphs.core.Node

.. raw:: html

   <hr/>

.. rubric:: Mixins
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.graphs.core.Attachable

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.graphs.graphers <uqbar--graphs--graphers>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.graphs.graphers.Grapher

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.graphs.html <uqbar--graphs--html>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: HTML Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.graphs.html.HRule
   ~uqbar.graphs.html.LineBreak
   ~uqbar.graphs.html.Table
   ~uqbar.graphs.html.TableCell
   ~uqbar.graphs.html.TableRow
   ~uqbar.graphs.html.Text
   ~uqbar.graphs.html.VRule

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.graphs.records <uqbar--graphs--records>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Record Field Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.graphs.records.RecordField
   ~uqbar.graphs.records.RecordGroup

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.io <uqbar--io>`
   :class: section-header

Tools for IO and file-system manipulation.

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.io.DirectoryChange
   ~uqbar.io.Profiler
   ~uqbar.io.RedirectedStreams
   ~uqbar.io.Timer

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.io.find_common_prefix
   ~uqbar.io.find_executable
   ~uqbar.io.relative_to
   ~uqbar.io.walk
   ~uqbar.io.write

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.iterables <uqbar--iterables>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.iterables.flatten
   ~uqbar.iterables.group_by_count
   ~uqbar.iterables.nwise
   ~uqbar.iterables.repeat_to_length
   ~uqbar.iterables.zip_cyclic

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.objects <uqbar--objects>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.objects.compare_objects
   ~uqbar.objects.get_hash
   ~uqbar.objects.get_repr
   ~uqbar.objects.get_vars
   ~uqbar.objects.new

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.sphinx <uqbar--sphinx>`
   :class: section-header

Sphinx extensions.

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.sphinx.api <uqbar--sphinx--api>`
   :class: section-header

Uqbar Sphinx API generation extension.

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.sphinx.api.logger_func
   ~uqbar.sphinx.api.on_builder_inited
   ~uqbar.sphinx.api.setup

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.sphinx.book <uqbar--sphinx--book>`
   :class: section-header

Uqbar Sphinx executable examples extension.

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.sphinx.book.on_build_finished
   ~uqbar.sphinx.book.on_builder_inited
   ~uqbar.sphinx.book.on_config_inited
   ~uqbar.sphinx.book.on_doctree_read
   ~uqbar.sphinx.book.setup
   ~uqbar.sphinx.book.skip_node

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.sphinx.inheritance <uqbar--sphinx--inheritance>`
   :class: section-header

Uqbar Sphinx inheritance graph extension.

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.sphinx.inheritance.InheritanceDiagram
   ~uqbar.sphinx.inheritance.inheritance_diagram

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.sphinx.inheritance.build_urls
   ~uqbar.sphinx.inheritance.html_visit_inheritance_diagram
   ~uqbar.sphinx.inheritance.latex_visit_inheritance_diagram
   ~uqbar.sphinx.inheritance.setup
   ~uqbar.sphinx.inheritance.skip

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.sphinx.style <uqbar--sphinx--style>`
   :class: section-header

Uqbar Sphinx styling extension.

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.sphinx.style.depart_classifier
   ~uqbar.sphinx.style.depart_definition
   ~uqbar.sphinx.style.depart_term
   ~uqbar.sphinx.style.handle_class
   ~uqbar.sphinx.style.handle_method
   ~uqbar.sphinx.style.on_builder_inited
   ~uqbar.sphinx.style.on_doctree_read
   ~uqbar.sphinx.style.setup
   ~uqbar.sphinx.style.visit_classifier
   ~uqbar.sphinx.style.visit_definition
   ~uqbar.sphinx.style.visit_term

.. raw:: html

   <hr/>

.. rubric:: :ref:`uqbar.strings <uqbar--strings>`
   :class: section-header

Tools for string manipulation.

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~uqbar.strings.ansi_escape
   ~uqbar.strings.delimit_words
   ~uqbar.strings.normalize
   ~uqbar.strings.to_dash_case
   ~uqbar.strings.to_snake_case