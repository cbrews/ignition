from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

short_description = "titan2 - Gemini Protocol Client Transport Library"
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='titan2',
    version='0.1.0.dev3',
    description=short_description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='GPLv3',
    url='https://github.com/cbrews/titan2',
    author='Chris Brousseau',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='gemini, client, request, socket',
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires='>=3.7, <4',
    install_requires=[
      'cryptography'
    ]
)