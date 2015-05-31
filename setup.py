#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='Leaf',
    version='0.1',
    description='Page objects support for salad and lettuce testing framework',
    author='Reza',
    author_email='m.roohian87@gmail.com',
    url='http://www.github.com/mroohian/leaf',
    packages=find_packages('src'),
    package_dir={'': 'src'}
)
