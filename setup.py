# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '0.0.1'

setup(
    name='order_center',
    version=version,
    description='order_center',
    author='keshav bhide',
    author_email='keshav.bhide.009@gmail.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=("frappe",),
)
