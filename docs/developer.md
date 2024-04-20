# Developing for Ignition

This section is a legacy document preserved for software developers who are interested in forking this project.

## Contributing

Ignition is no longer accepting contributions.  Please consider forking this library.

## Developing

### Local Environment Setup

I recommend using `pyenv` and `virtualenv` locally to manage your python environment.  Once you have [pyenv](https://github.com/pyenv/pyenv) installed (with [shell extensions](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv)), you can `cd` into the `ignition` directory you should be able to run:
```bash
$ python --version
Python 3.10.4
```

Run the following command to setup a local python3 virtual environment on first run:
```bash
$ python -m venv venv
created virtual environment ...
```

When starting development, initialize the virtual environment with:
```
$ . venv/bin/activate
```

Once your environment is running, you can install requirements:
```
$ pip install .[dev]
```

### Code Formatting Style
We are using a custom linting style enforced by `ruff` and `black`.  In order to make your life easier, I've
included pre-commit hooks that you can install once you've downloaded and installed requirements.

```
$ pre-commit install
```

Code style will be updated on commit.

### Unit Testing
Unit testing is build through `pytest`.  Unit test can be run by:
```
$ python -m pytest
```
