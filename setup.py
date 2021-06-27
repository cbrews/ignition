'''
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one
at http://mozilla.org/MPL/2.0/.
'''
import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')
requirements = (here / 'requirements.txt').read_text(encoding='utf-8').splitlines()

setup(
  long_description=long_description,
  long_description_content_type='text/markdown',
  packages=find_packages(exclude=["tests",
                                  "tests.*",
                                  "examples"]),
  python_requires='>=3.7, <4',
  install_requires=requirements
)
