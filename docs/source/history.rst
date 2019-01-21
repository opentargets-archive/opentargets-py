.. _history:

Changelog
=========

3.1.14
------
- two new endpoints through the client as get_target and get_disease

3.1.0
-----
- added SSL ceritificate customisation
- added HTTP and SOCKS proxies support

3.0.0
-----
Compatible with REST API release 3.0
- added `get_similar_target` and `get_similar_disease` methods
- added ability to return json objects as addict Dictionaries
- use next param to paginate when possible
- retry on server side errors to make the connection more reliable

2.0.0
-----
Compatible with REST API release 2.0
- added option to save the json query result to a local file
- bugfixes

1.2.0
-----
- added statistics module to allow score computation on subset of data
- improved fetching efficiency for big requests
- to_json method works with iterator pattern
- improved docs, and changed to Google Style
- set specific user agent for requests sent
- added methods to explore the REST API documentation and available endpoints
- added ping method to check for the api to be reachable

1.2.0b1
-------

- Added option to export data as JSON, csv, excel or pandas dataframe. (optional dependency for pandas and xlwt)
- Fixed post calls and automatically switch to post for a large request



1.2.0a2
-------

- Added filtering support to IterableResult
- Added parsing of swagger YAML for query validation

Minor:

- bugfixes
- improved tests
- improved docs

1.2.0a1
-------

- First alpha release
- Compatible with Rest API 1.2.0