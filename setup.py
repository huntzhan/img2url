#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (
    division, absolute_import, print_function, unicode_literals,
)

import codecs
import imp
import os
from setuptools import setup, find_packages

# load metadata.
metadata = imp.load_source(
    'metadata',
    os.path.join('img2url', 'metadata.py'),
)


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


def load_requirements(fname):
    # only handles a simple subset of requirements format.
    pkgs = []
    for line in read(fname).split(os.linesep):
        if not line or line.startswith('#'):
            continue
        pkgs.append(line)
    return pkgs


setup(
    # informations.
    name=metadata.NAME,
    version=metadata.VERSION,
    author=metadata.AUTHORS[0],
    author_email=metadata.EMAILS[0],
    maintainer=metadata.AUTHORS[0],
    maintainer_email=metadata.EMAILS[0],
    license=metadata.LICENSE,
    url=metadata.URL,
    description=metadata.DESCRIPTION,
    long_description=read('README.md'),
    # https://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    # critical configurations.
    packages=find_packages(),
    install_requires=load_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'img2url = img2url.main:entry_point'
        ],
    },
)
