.. _history:

Changelog
=========

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