.. _uqbar--graphs--core:

core
====

.. automodule:: uqbar.graphs.core

.. currentmodule:: uqbar.graphs.core

.. autoclass:: Attachable
   :show-inheritance:

   .. automethod:: attach
   .. autoproperty:: edges

.. autoclass:: Edge
   :show-inheritance:

   .. automethod:: __format__
   .. automethod:: __format_graphviz__
   .. automethod:: attach
   .. autoproperty:: attributes
   .. automethod:: detach
   .. autoproperty:: head
   .. autoproperty:: head_graph_order
   .. autoproperty:: head_port_position
   .. autoproperty:: is_directed
   .. autoproperty:: tail
   .. autoproperty:: tail_graph_order
   .. autoproperty:: tail_port_position

.. autoclass:: Graph
   :show-inheritance:

   .. automethod:: __format__
   .. automethod:: __format_graphviz__
   .. autoproperty:: attributes
   .. autoproperty:: edge_attributes
   .. autoproperty:: is_cluster
   .. autoproperty:: is_digraph
   .. autoproperty:: node_attributes

.. autoclass:: Node
   :show-inheritance:

   .. automethod:: __format__
   .. automethod:: __format_graphviz__
   .. automethod:: attach
   .. autoproperty:: attributes
   .. autoproperty:: edges