#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from pyqp import __version__
# monkey patch os.link to force using symlinks
del os.link


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

README = open('README.md').read()

setup(
    name='pyqp',
    version=__version__,
    description='App that aggregates data over time',
    long_description=README,
    author='y',
    author_email='mbachows@akamai.com',
    url='https://github.com/michalbachowski/pyqp',
    packages=[
        'pyqp',
    ],
    package_dir={'pyqp': 'pyqp'},
    include_package_data=True,
    install_requires=[
    ],
    license="MIT",
    zip_safe=False,
    keywords='pyqp',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
)
