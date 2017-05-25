# opentargets-py
Python client for the Open Targets REST API at targetvalidation.org
[![Build Status](https://travis-ci.org/opentargets/opentargets-py.svg?branch=master)](https://travis-ci.org/opentargets/opentargets-py)
[![Documentation Status](https://readthedocs.org/projects/opentargets/badge/?version=latest)](http://opentargets.readthedocs.io/en/latest/?badge=latest)

Why should you use this client instead of the REST API directly?

- Include wrappers for all public methods, with query validation
- Tools for the most common calls (E.g. get data for a target gene symbol even if you do not know its Ensembl Gene Id)
- Supports automatic retrieval of paginated results with an iterator pattern
- Easily save query results as JSON, CSV or Excel file
- Handles Authentication
- Handles fair usage limits transparently
- Follows HTTP cache as set by the REST API
- Experimental HTTP2 support for better performance (beware the client library is in alpha)

This client is supported for Python 3.5 and upper.
Works on pythoon 2.7 on a best effort basis.

Documentation is available on [ReadTheDocs](http://opentargets.readthedocs.io/en/latest/?badge=latest)

QUICK START
===========

```python

from opentargets import OpenTargetsClient

ot = OpenTargetsClient()

search_result = ot.search('BRAF')
print(search_result[0])

a_for_target = ot.get_associations_for_target('BRAF')
for a in a_for_target:
    print(a['id'], a['association_score']['overall'])

a_for_disease = ot.get_associations_for_disease('cancer')

print(ot.get_association('ENSG00000157764-EFO_0005803')[0])

e_for_target = ot.get_evidence_for_target('BRAF')
print(e_for_target.to_json())

e_for_disease = ot.get_evidence_for_disease('medulloblastoma')

print(ot.get_evidence('5cf863da265c32d112ff4fc3bfc25ab3')[0])

print(ot.get_stats().info)

...

```


Contributing
============

To create a development environment:
```sh
git clone <this repo>
cd opentargets-py
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
Some guidelines:
- always start with `git checkout -b yourname-featureyouareadding`
- when ready, submit a PR
- Travis test have to pass before any PR can be merged

Releases will automatically deploy to pypi (thanks to travis) once a tag/release is created in the github console. 
