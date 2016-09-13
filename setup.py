#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='opentargets',
      version='1.2.0a1',
      description='Client for Open Targets REST API at targetvalidation.org',
      author='Andrea Pierleoni',
      author_email='andreap@ebi.ac.uk',
      maintainer='Open Targets Core Team',
      maintainer_email='support@targetvalidation.org',
      url='https://github.com/CTTV/opentargets-py',
      packages=find_packages(),
      license='Apache 2.0',
      download_url='https://github.com/CTTV/opentargets-py/tarball/1.2.0a1',
      keywords = ['opentargets', 'bioinformatics', 'python3'],
      include_package_data=True,
      install_requires=[
          'requests',
          'Click',
          'cachecontrol',
          'hyper >= 0.6.2',
          'namedtupled',
          'PyYAML'],
      entry_points='''
        [console_scripts]
        ot=opentargets.scripts.ot:cli
        ''',
      extras_require={
          'tests': [
              'nose',
              ],
          'docs': [
              'sphinx >= 1.4',
              'sphinx_rtd_theme']}
      )
