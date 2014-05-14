#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name="element",
    version="0.0.2",
    description="Element: a node based cms",
    author="Thomas Rabaix",
    author_email="thomas.rabaix@gmail.com",
    url="https://github.com/rande/python-element",
    packages = find_packages(),
    install_requires=[
        "markdown",
        "Jinja2",
        "tornado",
        "WTForms",
        "Werkzeug",
        "futures",
        "redis",
        "mailer",
        "ioc"
    ],
    include_package_data = True,
)