# opentargets-py
Python client for the Open Targets REST API at targetvalidation.org


Why should you use this client?

- Handles Authentication
- Handles fair usage limits
- Follow HTTP cache as set by the REST API
- Experimental HTTP2 support for better performance (beware the client library is in alpha)
- Supports automatic pagination
- Include wrappers for public methods
- Tools for the most common calls

This client is supported for Python 3.5 and upper.
Works on lower version (including python 2) on a best effort basis.


QUICK START
===========

```python

from opentargets import OpenTargetClient

ot = OpenTargetClient()

search_result = ot.search('BRAF')
print next(search_result)

as_for_target = ot.get_associations_for_target('BRAF')
for as in as_for_target:
    print(as.id, as.association_score['overall'])

as_for_disease = ot.get_associations_for_disease('cancer')

ev_for_target = ot.get_evidence_for_target('BRAF')
for ev in ev_for_target:
    print(ev.id)

ev_for_disease = ot.get_evidence_for_disease('cancer')

...

```