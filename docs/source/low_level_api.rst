.. _low_level_api:

Connection
==========
The opentargets client expose a `Connection` class that efficiently retireves data
from the REST API, supporting input validation, authentication, caching, and fair usage limits.
It is possible to call any endpoint of the API directly and the response is returned as an `IterableResult`.
With `IterableResult` instance it is possible to stream directly content from the REST API by using an interator pattern.
Data points are fetched dynamically and memory usage is optimised.

TODO