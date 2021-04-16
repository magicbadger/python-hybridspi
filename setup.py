#!/usr/bin/env python

from distutils.core import setup

setup(name='hybridspi',
      version='0.3.0',
      description='Hybrid Radio SPI implementation (ETSI TS 102 818, ETSI TS 102 371)',
      author='Ben Poor',
      author_email='magicbadger@gmail.com',
      url='https://github.com/magicbadger/python-hybridspi',
      license='GPL2',
      download_url='https://github.com/magicbadger/python-hybridspi/tarball/0.3.0',
      keywords=['dab', 'spi', 'hybrid', 'radio'],
      packages=['spi', 'spi.xml', 'spi.binary'],
      package_dir = {'' : 'src'},
      install_requires = ['python-dateutil', 'isodate', 'bitarray', 'asciitree'],
      scripts=['dump_binary']
)
