Uqbar
=====

Uqbar is a toolkit for building docs, graphs and more.

Uqbar comes with a set of ready-to-use Sphinx extensions:

.. autosummary::
   :nosignatures:

   uqbar.sphinx.api
   uqbar.sphinx.inheritance
   uqbar.sphinx.style

Its API auto-generation tools are extensible through subclassing, allowing for
extension customization:

.. autosummary::
   :nosignatures:

   uqbar.apis.APIBuilder
   uqbar.apis.ClassDocumenter
   uqbar.apis.FunctionDocumenter
   uqbar.apis.ModuleDocumenter
   uqbar.apis.RootDocumenter

Uqbar includes high-level tools for generating inheritance diagrams and
Graphviz graphs:

.. autosummary::
   :nosignatures:

   uqbar.apis.InheritanceGraph
   uqbar.graphs.Graph
   uqbar.graphs.Node
   uqbar.graphs.Edge

Consult Uqbar's API:

.. toctree::

   api/index
