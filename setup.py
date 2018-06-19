#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Minimal Python version sanity check (from IPython/JupyterHub)
from __future__ import print_function

import os
import sys

v = sys.version_info
if v[:2] < (3, 3):
    error = "ERROR: Jupyter Hub requires Python version 3.3 or above."
    print(error, file=sys.stderr)
    sys.exit(1)


if os.name in ("nt", "dos"):
    error = "ERROR: Windows is not supported"
    print(error, file=sys.stderr)

# At least we're on the python version we need, move on.
from setuptools import setup
from setuptools.command.bdist_egg import bdist_egg


class bdist_egg_disabled(bdist_egg):
    """Disabled version of bdist_egg

    Prevents setup.py install from performing setuptools' default easy_install,
    which it should never ever do.
    """

    def run(self):
        sys.exit(
            "Aborting implicit building of eggs. Use `pip install .`"
            " to install from source."
        )


pjoin = os.path.join
here = os.path.abspath(os.path.dirname(__file__))

# Get the current package version.
version_ns = {}
with open(pjoin(here, "sudospawner/version.py")) as f:
    exec(f.read(), {}, version_ns)

with open("README.md") as f:
    long_description = f.read()

setup_args = dict(
    name="sudospawner",
    packages=["sudospawner"],
    scripts=["scripts/sudospawner"],
    version=version_ns["__version__"],
    description="SudoSpawner: Spawner for JupyterHub using sudo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jupyter Development Team",
    author_email="jupyter@googlegroups.com",
    url="https://jupyter.org",
    license="BSD",
    platforms="Linux, Mac OS X",
    keywords=["Interactive", "Interpreter", "Shell", "Web"],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    install_requires=["jupyterhub>=0.7", "notebook"],
)

if __name__ == "__main__":
    setup(**setup_args)
