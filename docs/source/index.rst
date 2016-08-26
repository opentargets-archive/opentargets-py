.. opentargets documentation master file, created by
   sphinx-quickstart on Fri Aug 26 08:55:19 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. Biograpy documentation master file, created by
   sphinx-quickstart on Fri Apr 16 17:35:36 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=============================================================
opentargets - Python client for targetvalidation.org REST API
=============================================================

.. toctree::
   :maxdepth: 2


opentargets is the official python client for the [Open Targets REST API](https://www.targetvalidation.org/documentation/api) at [targetvalidation.org](https://www.targetvalidation.org)

This client allows you to query the API automatically taking care of handling all
the calls and returing data in a pythonic way.

Main advantages of using the client versus querying the REST API directly

- Include wrappers for all public methods
- Tools for the most common calls (E.g. get data for a target gene symbol even if you do not know its Ensembl Gene Id)
- Supports automatic retrieval of paginated results with an iterator pattern
- Handles Authentication
- Handles fair usage limits transparently
- Follows HTTP cache as set by the REST API
- Experimental HTTP2 support for better performance (beware the client library is in alpha)


This client is supported for Python 3.5 and upper.
Works on lower version (including python 2.7) on a best effort basis.
Take a look at the :ref:`tutorial` to have an idea of what you can do.


License
-------

Apache 2.0


Contact
-------

Andrea Pierleoni (andreap at ebi dot ac doc uk)
Open Targets Support (support at targetvalidation dot org)



Installation
------------
::

    $ pip install opentargets

You can also clone opentargets with Git by running:

::

    $ git clone git://github.com/CTTV/opentargets-py

Get the source code (or make your own fork) on GitHub : `CTTV/opentargets-py
<http://github.com/CTTV/opentargets-py>`_


Documentation
-------------

* :ref:`tutorial`
* :ref:`high_level_api`
* :ref:`low_level_api`
* :ref:`history`
