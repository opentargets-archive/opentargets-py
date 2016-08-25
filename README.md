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

a_for_target = ot.get_associations_for_target('BRAF')
for a in a_for_target:
    print(a.id, a.association_score['overall'])

a_for_disease = ot.get_associations_for_disease('cancer')

e_for_target = ot.get_evidence_for_target('BRAF')
for e in e_for_target:
    print(e.id)

e_for_disease = ot.get_evidence_for_disease('medulloblastoma')

...

```