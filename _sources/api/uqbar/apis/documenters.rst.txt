.. _uqbar--apis--documenters:

documenters
===========

.. automodule:: uqbar.apis.documenters

.. currentmodule:: uqbar.apis.documenters

.. autoclass:: ClassDocumenter
   :show-inheritance:

   .. autoproperty:: documentation_section
   .. automethod:: validate_client

.. autoclass:: FunctionDocumenter
   :show-inheritance:

   .. autoproperty:: documentation_section
   .. automethod:: validate_client

.. autoclass:: MemberDocumenter
   :show-inheritance:

   .. autoproperty:: client
   .. autoproperty:: documentation_section
   .. autoproperty:: package_path
   .. automethod:: validate_client

.. autoclass:: ModuleDocumenter
   :show-inheritance:

   .. autoproperty:: client
   .. autoproperty:: document_private_members
   .. autoproperty:: documentation_path
   .. autoproperty:: is_nominative
   .. autoproperty:: is_package
   .. autoproperty:: member_documenter_classes
   .. autoproperty:: member_documenters
   .. autoproperty:: member_documenters_by_section
   .. autoproperty:: module_documenters
   .. autoproperty:: package_name
   .. autoproperty:: package_path
   .. autoproperty:: reference_name

.. autoclass:: RootDocumenter
   :show-inheritance:

   .. autoproperty:: documentation_path
   .. autoproperty:: module_documenters
   .. autoproperty:: title