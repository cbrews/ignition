'''
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one
at http://mozilla.org/MPL/2.0/.
'''

from .globals import *
from .request import Request
from .response import (
  ClientCertRequiredResponse,
  ErrorResponse,
  InputResponse,
  PermFailureResponse,
  RedirectResponse,
  SuccessResponse,
  TempFailureResponse,
)
from .ssl.cert_store import CertStore
from .util import TimeoutManager

__version__ = '0.1.8'

__timeout = TimeoutManager(DEFAULT_REQUEST_TIMEOUT)
__cert_store = CertStore(DEFAULT_HOSTS_FILE)


def set_default_hosts_file(hosts_file):
  '''
  Set the default host file location where all of the certificate fingerprints
  are stored in order to support Trust-On-First-Use (TOFU) validation.
  By default, this file is stored in the root directory as your project in a
  file named `.known_hosts`. This can be updated to any readable location but
  should be stored somewhere persistent for security purposes.

  The format of this file is very similar to (but not identical to)
  the SSH `known_hosts` file.

  Parameters:
  * hosts_file: `string`

  '''
  __cert_store.set_hosts_file(hosts_file)


def set_default_timeout(timeout):
  '''
  Set the default timeout (in seconds) for all requests made via ignition.
  The default timeout is 30 seconds.

  Parameters:
  * timeout: `float`
  '''
  __timeout.set_default_timeout(timeout)


def url(request_url, referer=None):
  '''
  Given a *url* to a Gemini capsule, this returns a standardized,
  fully-qualified url to the Gemini capsule.  If a *referer* is
  provided, a dynamic URL is constructed by ignition to send a request
  to.  This logic follows URL definition behavior outlined in
  [RFC-3986](https://tools.ietf.org/html/rfc3986).

  This allows for the bulk of URL generation logic to be handled
  without ignition as opposed to within the business logic of the client.
  Here are some sample use cases:

  *Use Case 1: Automatically populate URL protocol*
  ```python
  ignition.url('//gemini.circumlunar.space') # => gemini://gemini.circumlunar.space
  ```

  *Use Case 2: Navigate to an absolute path*
  ```python
  ignition.url('/home', 'gemini://gemini.circumlunar.space') # => gemini://gemini.circumlunar.space/home
  ```

  *Use Case 3: Navigate to a relative path*
  ```python
  ignition.url('2', 'gemini://gemini.circumlunar.space/home') # => gemini://gemini.circumlunar.space/home/2
  ```

  *Use Case 4: Resolve paths with navigation*
  ```python
  ignition.url('../fun/', 'gemini://gemini.circumlunar.space/home/work/') # => gemini://gemini.circumlunar.space/home/fun/
  ```

  *Note:* if the user's intent is to generate a url to a Gemini capsule and then make a request,
  ignition recommends that you just provide the *url* and *referer* to `ignition.request()`, as
  that function encapsulates all of the logic within this method when making a request.  If you
  want to retrieve a URL from an already processed request, it is recommended to use
  `ignition.BaseResponse.url`, as that will store the URL that was actually used.  This method
  is only intended for use in constructing a URL but not generating a request.

  Parameters:
  * url: `string`
  * referer: `string` (optional)

  Returns: `string`
  '''
  dummy_req = Request(request_url, referer=referer)
  return dummy_req.get_url()


def request(request_url, referer=None, timeout=None, ca_cert=None):
  '''
  Given a *url* to a Gemini capsule, this performs a request to the specified
  url and returns a response (as a subclass of [ignition.BaseResponse](#ignitionbaseresponse))
  with the details associated to the response.  This is the interface that most
  users should use.

  If a *referer* is provided, a dynamic URL is constructed by ignition to send a
  request to. (*referer* expectes a fully qualified url as returned by
  `ignition.BaseResponse.url` or (less prefered) `ignition.url()`).
  Typically, in order to simplify the browsing experience, you should pass
  the previously requested URL as the referer to simplify URL construction logic.

  *See `ignition.url()` for details around url construction with a referer.*

  If a *timeout* is provided, this will specify the client timeout (in seconds)
  for this request.  The default is 30 seconds.  See also `ignition.set_default_timeout`
  to change the default timeout.

  If a *ca_cert* is provided, the certificate will be sent to the server as a CA CERT.
  You will need to provide the paths to both the certificate and the key in this case.

  Depending on the response from the server, as per Gemini specification, the
  corresponding response type will be returned.

  * If the response status begins with "1", the response type is `INPUT`,
    and will return a response of type [ignition.InputResponse](#ignitioninputresponse).
  * If the response status begins with "2", the response type is `STATUS`,
    and will return a response of type [ignition.SuccessResponse](#ignitionsuccessresponse).
  * If the response status begins with "3", the response type is `REDIRECT`,
    and will return a response of type [ignition.RedirectResponse](#ignitionredirectresponse).
  * If the response status begins with "4", the response type is `TEMPORARY FAILURE`,
    and will return a response of type [ignition.TempFailureResponse](#ignitiontempfailureresponse).
  * If the response status begins with "5", the response type is `PERMANENT FAILURE`,
    and will return a response of type [ignition.PermFailureResponse](#ignitionpermfailureresponse).
  * If the response status begins with "6", the response type is `CLIENT CERTIFICATE REQUIRED`,
    and will return a response of type [ignition.ClientCertRequiredResponse](#ignitionclientcertrequiredresponse).
  * If *no valid response* can be returned, ignition assigns a response type of "0"
    and returns a response of type [ignition.ErrorResponse](#ignitionerrorresponse).

  Parameters:
  * url: `string`
  * referer: `string` (optional)
  * timeout: `float` (optional)
  * ca_cert: `Tuple(cert_file, key_file)` (optional)

  Returns: `[ignition.BaseResponse](#ignitionbaseresponse)`
  '''

  req = Request(request_url, cert_store=__cert_store, request_timeout=__timeout.get_timeout(timeout), referer=referer, ca_cert=ca_cert)

  return req.send()
