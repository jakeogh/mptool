# -*- coding: utf-8 -*-

import sys

from setuptools import find_packages
from setuptools import setup

import fastentrypoints

if not sys.version_info[0] == 3:
    sys.exit("Python 3 is required. Use: 'python3 setup.py install'")

dependencies = ["icecream", "click"]

config = {
    "version": "0.1",
    "name": "mptool",
    "url": "https://github.com/jakeogh/mptool",
    "license": "ISC",
    "author": "Justin Keogh",
    "author_email": "github.com@v6y.net",
    "description": "messagepack functions for typed CLI IPC",
    "long_description": __doc__,
    "packages": find_packages(exclude=["tests"]),
    "package_data": {"mptool": ["py.typed"]},
    "include_package_data": True,
    "zip_safe": False,
    "platforms": "any",
    "install_requires": dependencies,
}

setup(**config)
