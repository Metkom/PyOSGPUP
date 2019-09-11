from __future__ import print_function
"""PyOSGPUP: Python, Open-source, Geophysical Eng. Univ. Pertamina

A python packages for geophysical data processing modeling, and interpretation.
"""

from os import path
from distutils.core import setup
from setuptools import find_packages

here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='PyOSGPUP',  # Required
    version='1.0.3',  # Required

    description='An open-source library for geophysical data processing, modeling, and interpretation based on Python.',  # Required
    long_description=long_description,  # Optional

    url='https://sites.google.com/site/metkomup/',  # Optional
    author='Komputasi Geofisika - Universitas Pertamina',  # Optional
    author_email='metkom.up@gmail.com',  # Optional

    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='geophysical data processing, modeling, and interpretation',  # Optional
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required

    install_requires=['numpy','matplotlib'],  # Optional

    # download_url="https://github.com/Metkom/PyOSGPUP",
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/Metkom/PyOSGPUP/issues',
        'Say Thanks!': 'https://sites.google.com/site/metkomup/pyosgpup',
        'Source': 'https://github.com/Metkom/PyOSGPUP',
    },
    platforms=["Windows","Linux","Mac OS-X"]

)
