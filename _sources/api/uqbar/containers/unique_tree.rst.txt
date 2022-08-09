.. _uqbar--containers--unique-tree:

unique_tree
===========

.. automodule:: uqbar.containers.unique_tree

.. currentmodule:: uqbar.containers.unique_tree

.. autoclass:: UniqueTreeContainer
   :show-inheritance:

   .. automethod:: __contains__
   .. automethod:: __iter__
   .. automethod:: __len__
   .. autoproperty:: children
   .. automethod:: depth_first
   .. automethod:: recurse

.. autoclass:: UniqueTreeDict
   :show-inheritance:

   .. automethod:: __contains__
   .. automethod:: __delitem__
   .. automethod:: __getitem__
   .. automethod:: __iter__
   .. automethod:: __setitem__
   .. automethod:: clear
   .. automethod:: depth_first
   .. automethod:: get
   .. automethod:: items
   .. automethod:: keys
   .. automethod:: pop
   .. automethod:: recurse
   .. automethod:: update
   .. automethod:: values

.. autoclass:: UniqueTreeList
   :show-inheritance:

   .. automethod:: __delitem__
   .. automethod:: __getitem__
   .. automethod:: __setitem__
   .. automethod:: append
   .. automethod:: extend
   .. automethod:: index
   .. automethod:: insert
   .. automethod:: pop
   .. automethod:: remove

.. autoclass:: UniqueTreeNode
   :show-inheritance:

   .. autoproperty:: depth
   .. autoproperty:: graph_order
   .. autoproperty:: name
   .. autoproperty:: parent
   .. autoproperty:: parentage
   .. autoproperty:: root

.. autoclass:: UniqueTreeSet
   :show-inheritance:

   .. automethod:: add
   .. automethod:: clear
   .. automethod:: pop
   .. automethod:: remove
   .. automethod:: update

.. autoclass:: UniqueTreeTuple
   :show-inheritance:

   .. automethod:: __getitem__
   .. automethod:: index