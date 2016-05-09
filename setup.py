#!/usr/bin/env python

from setuptools import setup

setup(name='linear-tsv',
      license='Apache',
      version='0.99.1',
      description='Line-oriented, tab-separated value format',
      author='Jason Dusek',
      author_email='jason.dusek@gmail.com',
      url='https://github.com/solidsnack/tsv',
      py_modules=['tsv'],
      install_requires=['six'],
      tests_require=['tox'],
      extras_require={'develop': 'tox'},
      classifiers=['License :: OSI Approved :: Apache Software License',
                   'Intended Audience :: Developers',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.5',
                   'Development Status :: 4 - Beta'])
