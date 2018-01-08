Uqbar
=====

Uqbar is a toolkit for building docs, graphs and more.

.. container:: svg-container

   .. inheritance-diagram:: uqbar

Sphinx extensions
-----------------

Uqbar comes with a set of ready-to-use Sphinx extensions:

.. autosummary::
   :nosignatures:

   uqbar.sphinx.api
   uqbar.sphinx.inheritance
   uqbar.sphinx.style

API auto-generation
-------------------

Its API auto-generation tools are extensible through subclassing, allowing for
extension customization:

.. autosummary::
   :nosignatures:

   uqbar.apis.APIBuilder
   uqbar.apis.ClassDocumenter
   uqbar.apis.FunctionDocumenter
   uqbar.apis.ModuleDocumenter
   uqbar.apis.RootDocumenter

Graphviz graphs
---------------

Uqbar includes high-level tools for generating inheritance diagrams and
Graphviz graphs:

.. autosummary::
   :nosignatures:

   uqbar.apis.InheritanceGraph
   uqbar.graphs.Graph
   uqbar.graphs.Node
   uqbar.graphs.Edge

Generic data-structures
-----------------------

.. autosummary::
   :nosignatures:

   uqbar.containers.DependencyGraph
   uqbar.containers.UniqueTreeNode
   uqbar.containers.UniqueTreeContainer

Context managers
----------------

.. autosummary::
   :nosignatures:

   uqbar.io.DirectoryChange
   uqbar.io.Profiler
   uqbar.io.RedirectedStreams
   uqbar.io.Timer

Consult Uqbar's API:

.. toctree::

   api/index
