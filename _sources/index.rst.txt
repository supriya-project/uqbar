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

   uqbar.apis.APIBuilder
   uqbar.apis.ClassDocumenter
   uqbar.apis.FunctionDocumenter
   uqbar.apis.ModuleDocumenter
   uqbar.apis.RootDocumenter

Graphviz graphs
---------------

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
   uqbar.containers.UniqueTreeList
   uqbar.containers.UniqueTreeSet

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
