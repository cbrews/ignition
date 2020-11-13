# Titan2
*In 1965, two astronauts flew into low earth orbit as part of the Gemini project, on a spacecraft powered by a Titan II rocket....* 

[PICTURE]

Titan2 is a simple but powerful transport library for Python3 clients using the recently designed [Gemini protocol](https://gemini.circumlunar.space/). This project intends to implement all of the [transport specifications](https://gemini.circumlunar.space/docs/specification.html) (sections 1-4) of the Gemini protocol and provide an easy-to-use interface, so as to act as a building block in a larger application.

If you're building a Python3 application that uses Gemini, Titan2 is your gateway to the stars, in very much the same way that [requests](https://requests.readthedocs.io/en/master/) is for HTTP and **gopherlib** is for Gopher.

In order to provide a best-in-class interface, this library does not implement the other parts of a typical client (including user interface and/or command line interface), and instead focuses on providing a robust programmatic API interface.  This project also assumes that different user interfaces will have different requirements for their display of text/gemini files (.gmi), and/or other mime-types, and as such considers this portion of the specification beyond the scope of this project.

## Project Status
![Python CI](https://github.com/cbrews/titan2/workflows/Python%20CI/badge.svg)

Titan2 is currently in pre-Alpha status, which means that subsequent releases could introduce breaking changes that affect the API.  You use Titan2 at your own risk and agree to monitor this repository for changes until a stable version is released.

## Installation
⚠ Titan2 currently supports Python versions 3.6 - 3.9.

You can currently install Titan2 via pip.  I typically recommend you do this within a [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

```bash
pip install titan2
```

If you prefer to install from source, you can clone and install the repository:

```bash
git clone https://github.com/cbrews/titan2.git
cd titan2
python3 setup.py install
```

## Simple Usage
The most basic usage of Titan2 allows the user to create a request and get a response back from a remote Gemini capsule:
```python
import titan2

# Fetch capsule content
response = titan2.request('//gemini.circumlunar.space')

# Print full response from remote capsule
print(response)
```

In **all** cases, Titan2 assumes that the specified endpoint and protocol will respond over the Gemini protocol, so even if you provide a different protocol or port, it will assume that the endpoint is a Gemini capsule.

## Key Features
✅ Titan2 currently supports the following features:
* Basic request/response connectivity to a Gemini-enabled server.
* Basic URL parsing mechanics to allow for specifying protocol, host, port, path, and query params, as per [RFC-3986](https://tools.ietf.org/html/rfc3986)
* Optional referer URL handling.  Titan2 allows the user to pass a path & referer URL and can construct the new path, to simplifying the resolution of links on a Gemini capsule page.
* Decoding of body responses on successful (20) response from Gemini servers.
* Trust-on-first-use certificate verification handling scheme.
* Fully-featured response objects for each response type.
* Robust, human-readable error management and custom error handling for failure cases beyond the scope of the protocol.

⚠ These features are not currently supported but may be supported in the future:
* Client certificates (coming soon)
* Alternative certificate verification schemes
* Automatic redirection following on 3x responses
* Automatic client certificate generation & resend on 6x responses

❌ The following Gemini features will *not* be supported by Titan2:
* Behavioral processing/handling of specific response types from Gemini capsules
* Body parsing & display of text/gemini mime types
* Command line interface
* Advanced session & history management
* Support for ANY other protocols

## Advanced Usage
More advanced request usage:

```python
import titan2

response = titan2.request('/servers', referer='//gemini.circumlunar.space:1965')

print("Got back response %s from %s" % (response.status, response.url))
# Got back a response 20 from gemini://gemini.circumlunar.space/servers

if not response.success():
  print("There was an error on the response.")
else:
  print(response.data())
```

Passing a referer:
```python
import titan2

response1 = titan2.request('//gemini.circumlunar.space')
response2 = titan2.request('home', referer=response1.url)

print(response2)
```

More advanced response validation:
```python
import titan2

response = titan2.request('//gemini.circumlunar.space')

if response.is_a(titan2.SuccessResponse):
  print('Success!')
  print(response.data())

elif response.is_a(titan2.InputResponse):
  print('Needs additional input: %s' % (response.data()))

elif response.is_a(titan2.RedirectResponse):
  print('Received response, redirect to: %s' % (response.data()))

elif response.is_a(titan2.TempFailureResponse):
  print('Error from server: %s' % (response.data())

elif response.is_a(titan2.PermFailureResponse):
  print('Error from server: %s' % (response.data())

elif response.is_a(titan2.ClientCertRequiredResponse):
  print('Client certificate required. %s' % (response.data())

elif response.is_a(titan2.ErrorResponse):
  print('There was an error on the request: %s' % (response.data())
```

## API Documentation
Full API documentation for Titan2 is available [here](./docs/api.md).

## Developers
Want to help contribute to Titan2?  See the [developer documentation](./docs/developer.md) for contribution guidelines, build processes, and testing.

## License
Titan2 is licensed under [GPLv3](./LICENSE).

## Thank you
* *solderpunk* for leading the design of the [Gemini protocol](https://gemini.circumlunar.space/docs/specification.html), without which this project would not have been possible.
* *Sean Conman* for writing the [Gemini torture tests](gemini://gemini.conman.org/test/torture), which were instrumental in initial client testing.
* *Michael Lazar* for his work on [Jetforce](https://github.com/michael-lazar/jetforce), which helped testing along the way.

🔭 Happy exploring!