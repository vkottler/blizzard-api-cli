#!/usr/bin/env python3

"""
Blizzard API CLI - Package distribution.

Vaughn Kottler 01/07/19
"""

# third-party
from setuptools import setup, find_packages

# internal
from blizzard_api import VERSION, DESCRIPTION

setup(name="blizzard_api",
      version=VERSION,
      packages=find_packages(),
      install_requires=["requests"],
      package_data={"": ["*.json"]},
      author="Vaughn Kottler",
      author_email="vaughnkottler@gmail.com",
      description=DESCRIPTION,
      url="https://github.com/vkottler/blizzard-api-cli",
      entry_points={"console_scripts": ["bapi = blizzard_api.client:main"]})
