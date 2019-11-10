# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os
import re
# reading package version (same way sqlalchemy does)
with open(os.path.join(os.path.dirname(__file__),'pyvalidate', '__init__.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'",re.S).match(v_file.read()).group(1)

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file (same way as in PyPa's sampleproject)
with open(os.path.join(here, 'README.txt'), encoding='utf-8') as f:
    readme = f.read()

setup(
    name="pyvalidate",
    version=package_version,
    author="Vahid Mardani",
    author_email="vahid.mardani@gmail.com",
    url="http://packages.python.org/pyvalidate",
    description="Python method's parameter validation library, as a pythonic decorator",
    maintainer="Vahid Mardani",
    maintainer_email="vahid.mardani@gmail.com",
    packages=["pyvalidate"],
    platforms=["any"],
    long_description=readme,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: Freeware",
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries'
        ],
    )
