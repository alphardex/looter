#!/usr/bin/env python
# coding=utf-8
import os
import looter
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='looter',
    version='v1.31',
    description=(
        'A python package aiming at avoiding unnecessary repetition in making common crawlers.'
    ),
    long_description=looter.__doc__,
    author='alphardex',
    author_email='2582347430@qq.com',
    maintainer='alphardex',
    maintainer_email='2582347430@qq.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    platforms=["all"],
    url='https://github.com/alphardex/looter',
    py_modules=['looter'],
    classifiers=[
    'Development Status :: 3 - Alpha',
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Intended Audience :: End Users/Desktop",
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    "Topic :: Internet",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Utilities"
    ],
    entry_points={
        'console_scripts': [
            'looter = looter.looter:cli',
        ]
    },
    install_requires=[
        'PyMySQL',
        'selenium',
        'requests',
        'lxml',
    ]
)