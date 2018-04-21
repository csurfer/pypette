#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file.
with open(path.join(here, "README.rst")) as f:
    long_description = f.read()

# Get package and author details.
about = {}
with open(path.join(here, "pypette", "__version__.py")) as f:
    exec(f.read(), about)

setup(
    # Name of the module
    name=about["__title__"],
    # Details
    version=about["__version__"],
    description=about["__description__"],
    long_description=long_description,
    # The project's main homepage.
    url=about["__url__"],
    # Author details
    author=about["__author__"],
    author_email=about["__author_email__"],
    # License
    license=about["__license__"],
    packages=[about["__title__"]],
    test_suite="tests",
    keywords="pipeline dev-tool threads multithreading python",
    classifiers=[
        # Intended Audience.
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        # License.
        "License :: OSI Approved :: MIT License",
        # Project maturity.
        "Development Status :: 3 - Alpha",
        # Operating Systems.
        "Operating System :: POSIX",
        # Supported Languages.
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        # Topic tags.
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=["crayons"],
)
