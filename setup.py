'''
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one 
at http://mozilla.org/MPL/2.0/.
'''

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

short_description = "ignition - Gemini Protocol Client Transport Library"
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='ignition-gemini',
    version='0.1.0.a5',
    description=short_description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MPL 2.0',
    url='https://github.com/cbrews/ignition',
    author='Chris Brousseau',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='gemini, client, request, socket',
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires='>=3.7, <4',
    install_requires=[
      'cryptography'
    ]
)