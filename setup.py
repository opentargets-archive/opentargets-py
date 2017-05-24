#!/usr/bin/env python

from distutils.core import setup
import opentargets as ot

setup(name=ot.__pkgname__,
      version=ot.__version__,
      description=ot.__description__,
      author=ot.__author__,
      url=ot.__homepage__,
      packages=['opentargets'],
      license=ot.__license__,
      download_url=ot.__homepage__ + '/archive/' + ot.__version__ + '.tar.gz',
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
