# opentargets-py
Python client for the Open Targets REST API at targetvalidation.org

[![Build Status](https://travis-ci.org/CTTV/opentargets-py.svg?branch=master)](https://travis-ci.org/CTTV/opentargets-py)
[![Documentation Status](https://readthedocs.org/projects/opentargets/badge/?version=latest)](http://opentargets.readthedocs.io/en/latest/?badge=latest)

Why should you use this client instead of the REST API directly?

- Handles Authentication
- Handles fair usage limits transparently
- Follows HTTP cache as set by the REST API
- Experimental HTTP2 support for better performance (beware the client library is in alpha)
- Supports automatic retrieval of paginated results with an iterator pattern
- Include wrappers for public methods
- Tools for the most common calls (E.g. get data for a target gene symbol even if you do not know its Ensembl Gene Id)

This client is supported for Python 3.5 and upper.
Works on lower version (including python 2) on a best effort basis.


QUICK START
===========

```python

from opentargets import OpenTargetsClient
from opentargets.conn import result_to_json

ot = OpenTargetsClient()

search_result = ot.search('BRAF')
print search_result[0]

a_for_target = ot.get_associations_for_target('BRAF')
for a in a_for_target:
    print(a['id'], a.association_score['overall'])

a_for_disease = ot.get_associations_for_disease('cancer')

print(ot.get_association('ENSG00000157764-EFO_0005803')[0])

e_for_target = ot.get_evidence_for_target('BRAF')
for e in e_for_target:
    print(result_to_json(e))

e_for_disease = ot.get_evidence_for_disease('medulloblastoma')

print(ot.get_evidence('5cf863da265c32d112ff4fc3bfc25ab3')[0])

print(ot.get_stats().info)

...

```