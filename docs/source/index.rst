.. opentargets documentation master file, created by
   sphinx-quickstart on Fri Aug 26 08:55:19 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

====================================================
opentargets - Python client for targetvalidation.org
====================================================

**opentargets** is the official python client for the `Open Targets REST API`_ at `api.opentargets.io`_

This client allows you to query the API automatically taking care of handling all
the calls and returning data in a pythonic way.

Main advantages of using the client versus querying the REST API directly

- Include wrappers for all public methods, with query validation
- Tools for the most common calls (E.g. get data for a target gene symbol even if you do not know its Ensembl Gene Id)
- Supports automatic retrieval of paginated results with an iterator pattern
- Easily save query results as JSON, CSV or Excel file
- Handles Authentication
- Handles fair usage limits transparently
- Follows HTTP cache as set by the REST API
- Experimental HTTP2 support for better performance (beware the client library is in alpha)


This client is supported for Python 3.5 and upper.
Works on lower version (including python 2.7) on a best effort basis.
Take a look at the :ref:`tutorial` to have an idea of what you can do.

.. _Open Targets REST API: https://www.targetvalidation.org/documentation/api
.. _targetvalidation.org: https://www.targetvalidation.org

License
-------

Apache 2.0


Contact
-------

- Author: Andrea Pierleoni (andreap at ebi dot ac dot uk)
- Support: Open Targets Support (support@targetvalidation.org)



Installation
------------
::

    pip install opentargets

or directly from github

::

    pip install git+git://github.com/CTTV/opentargets-py.git

Get the source code (or make your own fork) on GitHub : `CTTV/opentargets-py
<http://github.com/CTTV/opentargets-py>`_


Documentation
-------------

.. toctree::
   :maxdepth: 2

   tutorial
   high_level_api
   low_level_api
   modules
   history
