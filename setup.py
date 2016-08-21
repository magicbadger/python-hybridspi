#!/usr/bin/env python

from distutils.core import setup

setup(name='python-hybridspi',
      version='1.0.0',
      description='Hybrid Radio SPI implementation (ETSI TS 102 818 v3.1.1, ETSI TS 102 371 v.3.1.1)',
      author='Ben Poor',
      author_email='magicbadger@gmail.com',
      url='https://github.com/magicbadger/python-hybridspi',
      download_url='',
      keywords=['dab', 'spi', 'hybrid', 'radio'],
      packages=['spi', 'spi.xml', 'spi.binary'],
      package_dir = {'' : 'src'}
)
