#!/usr/bin/env python
"""
pip setup file
"""
from pydictchecker.config.global_config import __version__
from setuptools import setup


setup(
    name="PyDictChecker",
    version=__version__,
    description=(
        "PyDictChecker is a generic Python3 tool to run recursively through a dictionary and validate any kind of conditions in a given dictionary."
        "It is designed as a ''dictionary parser'' to verify element existence & value."
        "You can use ''human-readable'' rule to move on a node and check recursively and relatively any conditions (and sub-conditions)."
    ),
    author="Alexandre Veremme @ The POC Agency",
    author_email="alex@the-poc-agency.com",
    url="",
    download_url="",
    license="LICENSE",
    packages=["pydictchecker", "pydictchecker.config"],
    zip_safe=False
)