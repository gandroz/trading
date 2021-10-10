
import os
from setuptools import setup, find_packages
import trading


README = os.path.join(os.path.dirname(__file__), 'README.md')
VERSION = os.path.join(os.path.dirname(__file__), '__version__')
long_description = open(README).read() + '\n\n'
version = open(VERSION).read()

setup(name='trading',
      version=version,
      description="Trading backtest",
      long_description=long_description,
      author='Guillaume Androz',
      packages=find_packages(),
      include_package_data=True)