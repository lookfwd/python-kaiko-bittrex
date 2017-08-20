#!/usr/bin/env python

from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError, RuntimeError):
    long_description = open('README.md').read()

setup(name='kaikobittrex',
      version='1.0.3',
      packages=find_packages(),
      description='Python bindings for Kaiko Bittrex Historical trade data',
      long_description=long_description,
      author='Dimitrios Kouzis-Loukas',
      author_email='lookfwd@gmail.com',
      url='https://github.com/lookfwd/python-kaiko-bittrex',
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: MIT License',
          'Development Status :: 5 - Production/Stable',
          'Topic :: Office/Business :: Financial',
      ],
      test_suite="kaikobittrex.tests")
