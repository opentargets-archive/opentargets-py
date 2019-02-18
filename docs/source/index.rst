.. opentargets documentation master file, created by
   sphinx-quickstart on Fri Aug 26 08:55:19 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

========================================================================
opentargets-py - Python client for the `Open Targets Platform`_ REST API
========================================================================

**opentargets-py** is the official python client for the `Open Targets REST API`_.

This client allows you to query the API automatically handling all the calls and returning data in a pythonic way.

Main advantages of using the client versus querying the REST API directly:

- Include wrappers for all public methods, with query validation
- Tools for the most common calls (E.g. get data for a target gene symbol even if you do not know its Ensembl Gene Id)
- Supports automatic retrieval of paginated results with an iterator pattern
- Easily save query results as JSON, CSV or Excel file
- Handles Authentication
- Handles fair usage limits transparently
- Follows HTTP cache as set by the REST API
- Experimental HTTP2 support for better performance (beware the client library is in alpha)


This client is supported for Python 3.5 and higher.
Works with lower versions (including python 2.7) on a best effort basis.
Take a look at the :ref:`tutorial` to get an idea of what you can do.

.. _Open Targets REST API: https://platform-api.opentargets.io/v3/platform/docs/swagger-ui
.. _Open Targets Platform: https://www.targetvalidation.org

Installation
------------
::

    pip install opentargets

or directly from github

::

    pip install git+git://github.com/opentargets/opentargets-py.git

Get the source code (or make your own fork) on GitHub : `opentargets/opentargets-py
<http://github.com/opentargets/opentargets-py>`_


Documentation
-------------

.. toctree::
   :maxdepth: 2

   tutorial
   high_level_api
   low_level_api
   modules
   history
   
Support
-------

Open Targets Support (support@targetvalidation.org)

Copyright
---------

Copyright 2014-2019 Biogen, Celgene Corporation, EMBL - European Bioinformatics Institute, GlaxoSmithKline, Sanofi, Takeda Pharmaceutical Company and Wellcome Sanger Institute

This software was developed as part of the Open Targets project. For more information please see: http://www.opentargets.org

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either expressed or implied.
See the License for the specific language governing permissions and
limitations under the License.

