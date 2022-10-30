# Building ignition

We have upgraded to pyproject.toml build configuration.

Assuming you have already installed the virtual environment in the [developer steps](developer.md), all you need to do to build the package is to install the build dependencies:

```bash
$ python -m pip install .[build]
```

And then build with the native `build` package:
```bash
$ python -m build
```

Push to test pip:
```bash
$ python -m twine upload --repository testpypi dist/*
```

Push to real pip:
```bash
$ python -m twine upload dist/*
```

## References

* [Packaging Python Projects](https://packaging.python.org/tutorials/packaging-projects/)
* [PyPi](https://pypi.org/)
* [Test PyPi](test.pypi.org/)
