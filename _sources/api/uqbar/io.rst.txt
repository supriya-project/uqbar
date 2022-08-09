.. _uqbar--io:

io
==

.. automodule:: uqbar.io

.. currentmodule:: uqbar.io

.. autoclass:: DirectoryChange
   :show-inheritance:

   .. automethod:: __enter__
   .. automethod:: __exit__
   .. autoproperty:: directory
   .. autoproperty:: verbose

.. autoclass:: Profiler
   :show-inheritance:

   .. automethod:: __enter__
   .. automethod:: __exit__

.. autoclass:: RedirectedStreams
   :show-inheritance:

   .. automethod:: __enter__
   .. automethod:: __exit__
   .. autoproperty:: stderr
   .. autoproperty:: stdout

.. autoclass:: Timer
   :show-inheritance:

   .. automethod:: __enter__
   .. automethod:: __exit__
   .. autoproperty:: elapsed_time
   .. autoproperty:: enter_message
   .. autoproperty:: exit_message
   .. autoproperty:: start_time
   .. autoproperty:: stop_time
   .. autoproperty:: verbose

.. autofunction:: find_common_prefix

.. autofunction:: find_executable

.. autofunction:: relative_to

.. autofunction:: walk

.. autofunction:: write