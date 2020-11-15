# Building ignition

To build ignition, following these steps:

Ensure that your version is set in setup.py
```python
setup(
    name='ignition-gemini',
    version='0.1.0.dev1', # See versioning details here: https://www.python.org/dev/peps/pep-0440/
    # ...
)
```

Build package with setup.py and sdist/wheel:
```bash
$ python3 setup.py sdist bdist_wheel
```

Push to test pip:
```bash
$ python3 -m twine upload --repository testpypi dist/*
```

Push to real pip:
```bash
$ python3 -m twine upload dist/*
```

## References

* [Packaging Python Projects](https://packaging.python.org/tutorials/packaging-projects/)
* [PyPi](https://pypi.org/)
* [Test PyPi](test.pypi.org/)
