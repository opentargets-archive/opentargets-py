#!/usr/bin/env python

from distutils.core import setup

setup(name='opentargets',
      version='1.2.0a1',
      description='Client for Open Targets REST API at targetvalidation.org',
      author='Andrea Pierleoni',
      author_email='andreap@ebi.ac.uk',
      maintainer='Open Targets Core Team',
      maintainer_email='support@targetvalidation.org',
      url='https://github.com/CTTV/opentargets-py',
      packages=['opentargets'],
      license='Apache 2.0',
      download_url='https://github.com/CTTV/opentargets-py/tarball/1.2.0a1',
      keywords = ['opentargets', 'bioinformatics', 'python3']
      )