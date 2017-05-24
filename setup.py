#!/usr/bin/env python

from distutils.core import setup
from opentargets import __pkgname__, __version__, \
     __description__, __author__, __homepage__, __license__


setup(name=__pkgname__,
      version=__version__,
      description=__description__,
      author=__author__,
      url=__homepage__,
      packages=['opentargets'],
      license=__license__,
      download_url=__homepage__ + '/archive/' + __version__ + '.tar.gz',
      keywords=['opentargets', 'bioinformatics', 'python3'],
      install_requires=[
          'requests>=2.11.1,<3.0',
          'cachecontrol==0.11.6',
          'hyper==0.7.0',
          'h2==2.4.2',
          'future==0.16.0',
          'PyYAML'],
      extras_require={
          'tests': [
              'nose',
              'pandas',
              'xlwt',
              'tqdm'
              ],
          'docs': [
              'sphinx >= 1.4',
              'sphinx_rtd_theme']}
      )
