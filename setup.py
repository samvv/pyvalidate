
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md')) as f:
    readme = f.read()

setup(
    name="pyvalidate",
    version='2.0.0',
    description="A data validation library for Python 3",
    long_description=readme,
    long_description_content_type='text/markdown',
    url="http://packages.python.org/pyvalidate",
    author="Sam Vervaeck",
    author_email="samvv@pm.me",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.5, <4',
    install_requires=['gast'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries'
    ],
    keywords='validation validator schema tool web-api data',
    project_urls={
        'Bug Reports': 'https://github.com/samvv/pyvalidate/issues',
        'Source': 'https://github.com/samvv/pyvalidate/'
    }
)

