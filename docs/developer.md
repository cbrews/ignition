# Developing for Ignition

## Contributing Guidelines

### Code of Conduct

### Bug Reporting

### Feature Requests

### How to Contribute Code

## Developing

### Local Environment Setup

I recommend using `virtualenv` locally to manage your python environment.  Run the following command to setup a local python3 virtual environment on first run:
```
$ python3 -m virtualenv ./venv
created virtual environment ...
```

When starting development, initialize the virtual environment with:
```
$ . venv/bin/activate
```

Check your python version:
```
$ python --version
Python 3.8.5
```

Once your environment is running, you can install requirements:
```
$ pip -r requirements.txt
```

### Code Formatting Style
No linting or requirements are currently enforced.  I understand my style is a bit divergent from standard Python style; I hope to clean this up soon.

### Unit Testing
Unit testing is build through `pytest`.  Unit test can be run by:
```
$ pytest
```

### Version testing
Version testing is currently handled within Github actions.
