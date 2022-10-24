Uqbar
=====

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

Uqbar is a toolkit for building docs, graphs and more.

.. container:: svg-container

   .. inheritance-diagram:: uqbar

Sphinx extensions
-----------------

.. autosummary::
   :nosignatures:

   uqbar.sphinx.api
   uqbar.sphinx.book
   uqbar.sphinx.inheritance
   uqbar.sphinx.style

API auto-generation
-------------------

.. autosummary::
   :nosignatures:

   uqbar.apis.builders.APIBuilder
   uqbar.apis.documenters.ClassDocumenter
   uqbar.apis.documenters.FunctionDocumenter
   uqbar.apis.documenters.ModuleDocumenter
   uqbar.apis.documenters.RootDocumenter

Graphviz graphs
---------------

.. autosummary::
   :nosignatures:

   uqbar.apis.graphs.InheritanceGraph
   uqbar.graphs.core.Graph
   uqbar.graphs.core.Node
   uqbar.graphs.core.Edge

Generic data-structures
-----------------------

.. autosummary::
   :nosignatures:

   uqbar.containers.dependency_graph.DependencyGraph
   uqbar.containers.unique_tree.UniqueTreeNode
   uqbar.containers.unique_tree.UniqueTreeList
   uqbar.containers.unique_tree.UniqueTreeSet

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
