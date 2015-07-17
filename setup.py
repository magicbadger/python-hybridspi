#!/usr/bin/env python

from distutils.core import setup

setup(name='python-hybridspi',
      version='1.0.0',
      description='Hybrid Radio SPI implementation',
      author='Ben Poor',
      author_email='magicbadger@gmail.com',
      packages=['spi', 'spi.xml'],
      package_dir = {'' : 'src'}
)
