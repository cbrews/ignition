# Ignition: Python3 Gemini Protocol Client Transport Library

![This is Gemini Control.  We're at T-1 minute, T-60 seconds and counting.  T-45 seconds and counting.  The range holding a final status check.  T-30 seconds.  Recorders have gone to fast speed.  Twenty seconds.  Fifteen seconds.  Ten, nine, eight, seven, six, five, four, three, two, one zero.  Ignition.](docs/img/transcript-1.png)

Ignition is a simple but powerful transport library for Python3 clients using the recently designed [Gemini protocol](https://gemini.circumlunar.space/). This project intends to implement all of the [transport specifications](https://gemini.circumlunar.space/docs/specification.html) (sections 1-4) of the Gemini protocol and provide an easy-to-use interface, so as to act as a building block in a larger application.

If you're building a Python3 application that uses Gemini, Ignition is your gateway to the stars, in very much the same way that [requests](https://requests.readthedocs.io/en/master/) is for HTTP and **gopherlib** is for Gopher.

In order to provide a best-in-class interface, this library does not implement the other parts of a typical client (including user interface and/or command line interface), and instead focuses on providing a robust programmatic API interface.  This project also assumes that different user interfaces will have different requirements for their display of text/gemini files (.gmi), and/or other mime-types, and as such considers this portion of the specification beyond the scope of this project.

In addition, in order to provide stability and simplicity, minimal third-party dependencies are required for Ignition.

## Project Status
![GitHub release (latest by date)](https://img.shields.io/github/v/release/cbrews/ignition?label=ignition)
[![CI v2](https://github.com/cbrews/ignition/actions/workflows/ci-v2.yml/badge.svg)](https://github.com/cbrews/ignition/actions/workflows/ci-v2.yml)

![The status is good to go.  This is Gemini Control.](docs/img/transcript-2.png)

Ignition is currently in prerelease.  You can use Ignition today at your own risk, please monitor this repository for changes until version 1.0 is released.  Please be advised that there may be breaking changes in the API until that time.

You can see ignition in action at [gemini.cbrews.xyz](https://gemini.cbrews.xyz).

## Installation
⚠ Ignition currently supports Python versions 3.7 - 3.10.

Ignition can be installed via [PIP](https://pypi.org/project/ignition-gemini/).  You should install it in alignment with your current development process; if you do not have a build process yet, I recommend you install within a [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

```bash
pip install ignition-gemini
```

If you prefer to install from source, you can clone and install the repository:

```bash
git clone https://github.com/cbrews/ignition.git
cd ignition
python3 setup.py install
```

## Simple Usage
The most basic usage of Ignition allows the user to create a request and get a response back from a remote Gemini capsule:
```python
import ignition

# Fetch capsule content
response = ignition.request('//gemini.circumlunar.space')

# Get status from remote capsule
print(response.status)

# Get response information from remote capsule
print(response.data())
```
[source](examples/simple-usage.py)

In **all** cases, Ignition assumes that the specified endpoint and protocol will respond over the Gemini protocol, so even if you provide a different protocol or port, it will assume that the endpoint is a Gemini capsule.

## Key Features

![This is Gemini Control.  The conversation between pilot and ground so far in this filght has largely been confined to the normal type of test pilot talk that you would expect.](docs/img/transcript-3.png)

✅ Ignition currently supports the following features:
* Basic request/response connectivity to a Gemini-enabled server.
* Basic URL parsing mechanics to allow for specifying protocol, host, port, path, and query params, as per [RFC-3986](https://tools.ietf.org/html/rfc3986)
* Optional referer URL handling.  Ignition allows the user to pass a path & referer URL and can construct the new path, to simplifying the resolution of links on a Gemini capsule page.
* Basic decoding of body responses on successful (20) response from Gemini servers.
* Trust-on-first-use certificate verification handling scheme using key signatures.
* Fully-featured response objects for each response type.
* Standardized & robust, human-readable error management.
* Custom error handling for networking failure cases beyond the scope of the protocol.

❌ The following Gemini features will *not* be supported by Ignition:
* Behavioral processing/handling of specific response types from Gemini capsules, including:
  * Generation of client certificates & automatic resubmission.
  * Automatic redirection following on 3x responses.
* Advanced body response rendering and/or display of text/gemini mime types.
* Command line or GUI interface.
* Advanced session & history management.
* Support for other protocols.

⚠ These features are not currently supported but may be supported in the future:
* Non-verified certificate scheme
* Improved TOFU scenarios

## Advanced Usage
More advanced request usage:

```python
import ignition

response = ignition.request('/software', referer='//gemini.circumlunar.space:1965')

print("Got back response %s from %s" % (response.status, response.url))
# Got back a response 20 from gemini://gemini.circumlunar.space/software

if not response.success():
  print("There was an error on the response.")
else:
  print(response.data())
```

Passing a referer:
```python
import ignition

response1 = ignition.request('//gemini.circumlunar.space')
response2 = ignition.request('software', referer=response1.url)

print(response2)
```
[source](examples/using-referer.py)

More advanced response validation:
```python
import ignition

url = '//gemini.circumlunar.space'
response = ignition.request(url)

if response.is_a(ignition.SuccessResponse):
  print('Success!')
  print(response.data())

elif response.is_a(ignition.InputResponse):
  print('Needs additional input: %s' % (response.data()))

elif response.is_a(ignition.RedirectResponse):
  print('Received response, redirect to: %s' % (response.data()))

elif response.is_a(ignition.TempFailureResponse):
  print('Error from server: %s' % (response.data()))

elif response.is_a(ignition.PermFailureResponse):
  print('Error from server: %s' % (response.data()))

elif response.is_a(ignition.ClientCertRequiredResponse):
  print('Client certificate required. %s' % (response.data()))

elif response.is_a(ignition.ErrorResponse):
  print('There was an error on the request: %s' % (response.data()))
```
[source](examples/advanced-usage.py)

Finally, the module exposes `DEBUG` level logging via standard python capabilities.  If you are having trouble with the requests, enable debug-level logging with:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## API Documentation
Full API documentation for Ignition is available [here](./docs/api.md).

## Developers

![There are a few reports from the pilots.  They are simply identifying their flight plan very carefully.  Four minutes into the flight, Gordon Cooper just told Grissom that he is looking mighty good.  Gus gave him a reasuring laugh.  A very calm pilot in command of that spacecraft.](docs/img/transcript-4.png)

Want to help contribute to Ignition?  See the [developer documentation](./docs/developer.md) for contribution guidelines, build processes, and testing.

The developer documentation is still being completed, if you have specific questions, please open tickets within this project.

## License
Ignition is licensed under [Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/).

Copyright 2020-2021 by [Chris Brousseau](https://github.com/cbrews).

## Thank you
* *solderpunk* for leading the design of the [Gemini protocol](https://gemini.circumlunar.space/docs/specification.html), without which this project would not have been possible.
* *Sean Conman* for writing the [Gemini torture tests](gemini://gemini.conman.org/test/torture), which were instrumental in initial client testing.
* *Michael Lazar* for his work on [Jetforce](https://github.com/michael-lazar/jetforce), which helped testing along the way.

🔭 Happy exploring!
