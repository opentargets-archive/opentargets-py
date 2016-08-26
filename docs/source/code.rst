.. _code:

Documentation for the Code
**************************


High Level Client
=================

This module communicate with the Open Targets REST API with a simple client, and requires not knowledge of the API.

.. automodule:: opentargets
   :members:

.. autoclass:: opentargets.OpenTargetsClient
	:members:
	:show-inheritance:
	:inherited-members:
	:undoc-members:

Low Level Client
================

This module abstracts the connection to the Open Targets REST API to simplify its usage.
Can be used directly but requires some knowledge of the API.

.. automodule:: opentargets.conn
   :members:

.. autoclass:: opentargets.conn.Connection
	:members:
	:show-inheritance:
	:inherited-members:
	:undoc-members: