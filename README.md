# opentargets-py
Python client for the Open Targets REST API at api.opentargets.io
[![Build Status](https://travis-ci.com/opentargets/opentargets-py.svg?branch=master)](https://travis-ci.com/opentargets/opentargets-py)
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
- Support for advanced SSL and proxy configuration

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
## How to contribute:
1. (if you are not part of the open targets team) fork the repo
2. branch from master, always start with `git checkout -b yourname-featureyouareadding`
2. code
3. push your branch and submit a PR
4. ask for reviews for your PR
5. Travis tests have to pass
6. Your PR is approved and merged

## How to release
1. Draft a new release https://github.com/opentargets/opentargets-py/releases/new
2. add a tag using semantic versioning, pointing to `master`
3. Press publish

Releases will automatically deploy to pypi (thanks to travis) once they are created in the github console.
