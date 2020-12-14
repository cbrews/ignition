# Developing for Ignition

This section is still under development!

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

## Contributing Guidelines

### Code of Conduct
First and foremost, be a good citizen of the Open Source community and the Geminisphere.  Please be friendly, respectful, professional, and patient with other members of the communities.

Be welcoming to new members; remember that no one has exactly the same background and experience as you, and only by elevating other perspectives can we truly develop the best software and uncover the best solutions.

We will always appreciate good faith conversation and contribution in the community.  In addition, we ask you to be resourceful, curious, and thoughtful in all engagement on this project.  Disagreements may occur; in such cases any discussion is a learning opportunity.

There will always be issues with code, in such scenarios please know that the developer is interested in engaging in remediation or resolution at their convenience, given that this is in no means a primary source of business or income.

The developer will make a best effort to maintain backwards compatibility after release 1.0 as possible but in certain circumstances such compatibility may not be possible.

### Bug Reporting
Please use the ticketing system within Github for any issues.

More details coming soon!

### Feature Requests
Please use the ticketing system and open a ticket before opening a PR.

More details coming soon!

### How to Contribute Code
Please use the pull request system within Github for any contributions.

More details coming soon!
