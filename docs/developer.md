# Developing for Ignition

This section is for software developers who are interested in contributing to the `ignition` project.

## Contributing

*Bugs*: If you find a problem with the software, you may open a Github issue for the bug.  Additionally, if you have found a solution, please go ahead and open a PR with a fix.  A Github issue is not required if you are able to just open a PR.  Please ensure that:
* The issue is clearly described (what versions of Python are affected, if not all)
* Provide clear steps on how to test, if applicable
* All linting and tests pass
* Documentation is updated as needed

*Features*: Please feel free to pull any issue to for feature development and create a PR.  Please note: due to the intentional small scope of this project, we are not currently accepting pull requests for new features without a corresponding issue approved by the core developer.  

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
$ pip -r requirements.txt -r requirements-dev.txt
```

### Code Formatting Style
We are using a custom linting style enforced by `pylint` and `yapf`.  In order to make your life easier, I've
included pre-commit hooks that you can install once you've downloaded and installed requirements.

```
$ pre-commit install
```

Code style will be updated on commit.

### Unit Testing
Unit testing is build through `pytest`.  Unit test can be run by:
```
$ pytest
```

### Version testing
Version testing is currently handled within Github actions.

## Contributing Guidelines

### Code of Conduct
First and foremost, be a good citizen of the Open Source community and of the Geminisphere.  Please be friendly, respectful, professional, and patient with other participants in the community.

Be welcoming to new members; remember that no one has the same background and experience as you. By elevating other perspectives, we can uncover the best solutions and develop the best software.

We will always appreciate good faith conversation and contribution in the community.  In addition, we ask you to come with these values: be thoughtful, resourceful, and curious when you engage on this project.  Disagreements may occur; but through maintaining these values, any disagreement can become a learning opportunity.

There will always be bugs and issues with code. In the event of proposed change, please keep in mind that the core developer will be able to remediate and/or resolve any issues at their convenience, given that this project is in no means a primary business or primary source of income.

The core developer will make a best effort to maintain backwards compatibility after release 1.0 as possible but in certain circumstances such compatibility may not be possible.
