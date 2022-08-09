.. _uqbar--book--extensions:

extensions
==========

.. automodule:: uqbar.book.extensions

.. currentmodule:: uqbar.book.extensions

.. autoclass:: Extension
   :show-inheritance:

   .. automethod:: add_option
   .. automethod:: depart_block_text
   .. automethod:: setup_console
   .. automethod:: setup_sphinx
   .. automethod:: teardown_console
   .. automethod:: visit_block_html
   .. automethod:: visit_block_latex
   .. automethod:: visit_block_text

.. autoclass:: GraphExtension
   :show-inheritance:

   .. automethod:: clean_svg
   .. automethod:: render_image
   .. automethod:: setup_console
   .. automethod:: setup_sphinx
   .. automethod:: to_docutils
   .. automethod:: visit_block_html