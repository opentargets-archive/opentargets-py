.. opentargets documentation master file, created by
   sphinx-quickstart on Fri Aug 26 08:55:19 2016.
   Feel free to adapt this file but make sure that it maintains the root `toctree` directive, at least.

====================================================
opentargets - Python client for targetvalidation.org
====================================================

**opentargets** is the official python client for the `Open Targets REST API`_ at `targetvalidation.org`_

This client allows you to query our API where all the calls and returning data are carried out in a pythonic way: 

What are the main advantages of using the Py client over our REST API? The Pyopentargets (or the other name):

- includes wrappers for all public methods, with query validation
- offers tools for the most common calls such as how to get data for the gene symbol of a target even if you do not know its Ensembl Gene ID
- supports automatic retrieval of paginated results with an iterator pattern
- handles authentication (no need for an API key??!?!)
- manages the limits of fair usage in a transparent fashion
- follows HTTP cache as set by our REST API
- supports HTTP2 for better performance (note this is experimental where the client library is in alpha)


The minimum requirement for our client is Python 3.5. It may work on previous versions (including python 2.7) on a best effort basis.
Take a look at our :ref:`tutorial` to have an idea of what you can do with the Pyopentargets.

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
<http://github.com/CTTV/opentargets-py>`_ (I've seen 'Fork me on GitHub' thingy here http://www.restapitutorial.com/lessons/whatisrest.html as a red 'banner' on the top right. It did catch my attention. It may be something we want to do...)


Documentation (Is this for the API? Can we make this clearer please?)
-------------

.. toctree::
   :maxdepth: 2

   tutorial
   high_level_api
   low_level_api
   modules
   history
