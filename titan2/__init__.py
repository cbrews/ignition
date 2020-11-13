'''
titan2 - Gemini Protocol Client Transport Library
Copyright (C) 2020  Chris Brousseau

titan2 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

titan2 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with titan2.  If not, see <https://www.gnu.org/licenses/>.
'''

from .globals import *
from .cert_store import CertStore
from .request import Request
from .response import ErrorResponse, InputResponse, SuccessResponse, RedirectResponse, TempFailureResponse, PermFailureResponse, ClientCertRequiredResponse

__timeout = DEFAULT_REQUEST_TIMEOUT
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
  Set the default timeout (in seconds) for all requests made via titan2.
  The default timeout is 30 seconds.

  Parameters:
  * timeout: `float`
  '''
  __timeout = timeout

def url(url, referer=None):
  '''
  Given a *url* to a Gemini capsule, this returns a standardized, 
  fully-qualified url to the Gemini capsule.  If a *referer* is 
  provided, a dynamic URL is constructed by titan2 to send a request 
  to.  This logic follows URL definition behavior outlined in 
  [RFC-3986](https://tools.ietf.org/html/rfc3986).

  This allows for the bulk of URL generation logic to be handled 
  without titan2 as opposed to within the business logic of the client.  
  Here are some sample use cases:

  *Use Case 1: Automatically populate URL protocol*
  ```python
  titan2.url('//gemini.circumlunar.space') # => gemini://gemini.circumlunar.space
  ```

  *Use Case 2: Navigate to an absolute path*
  ```python
  titan2.url('/home', 'gemini://gemini.circumlunar.space') # => gemini://gemini.circumlunar.space/home
  ```

  *Use Case 3: Navigate to a relative path*
  ```python
  titan2.url('2', 'gemini://gemini.circumlunar.space/home') # => gemini://gemini.circumlunar.space/home/2
  ```

  *Use Case 4: Resolve paths with navigation*
  ```python
  titan2.url('../fun/', 'gemini://gemini.circumlunar.space/home/work/') # => gemini://gemini.circumlunar.space/home/fun/
  ```

  *Note:* if the user's intent is to generate a url to a Gemini capsule and then make a request, 
  titan2 recommends that you just provide the *url* and *referer* to `titan2.request()`, as 
  that function encapsulates all of the logic within this method when making a request.  If you 
  want to retrieve a URL from an already processed request, it is recommended to use 
  `titan2.BaseResponse.url`, as that will store the URL that was actually used.  This method 
  is only intended for use in constructing a URL but not generating a request.

  Parameters:
  * url: `string`
  * referer: `string` (optional)

  Returns: `string`
  '''
  dummy_req = Request(url, referer=referer)
  return dummy_req.get_url()

def request(url, referer=None, timeout=None):
  '''
  Given a *url* to a Gemini capsule, this performs a request to the specified 
  url and returns a response (as a subclass of [titan2.BaseResponse](#titan2baseresponse)) 
  with the details associated to the response.  This is the interface that most 
  users should use.

  If a *referer* is provided, a dynamic URL is constructed by titan2 to send a 
  request to. (*referer* expectes a fully qualified url as returned by 
  `titan2.BaseResponse.url` or (less prefered) `titan2.url()`). 
  Typically, in order to simplify the browsing experience, you should pass 
  the previously requested URL as the referer to simplify URL construction logic.

  *See `titan2.url()` for details around url construction with a referer.*

  If a *timeout* is provided, this will specify the client timeout (in seconds) 
  for this request.  The default is 30 seconds.  See also `titan2.set_default_timeout` 
  to change the default timeout.

  Depending on the response from the server, as per Gemini specification, the 
  corresponding response type will be returned.

  * If the response status begins with "1", the response type is `INPUT`, and will return a response of type [titan2.InputResponse](#titan2inputresponse).
  * If the response status begins with "2", the response type is `STATUS`, and will return a response of type [titan2.SuccessResponse](#titan2successresponse).
  * If the response status begins with "3", the response type is `REDIRECT`, and will return a response of type [titan2.RedirectResponse](#titan2redirectresponse).
  * If the response status begins with "4", the response type is `TEMPORARY FAILURE`, and will return a response of type [titan2.TempFailureResponse](#titan2tempfailureresponse).
  * If the response status begins with "5", the response type is `PERMANENT FAILURE`, and will return a response of type [titan2.PermFailureResponse](#titan2permfailureresponse).
  * If the response status begins with "6", the response type is `CLIENT CERTIFICATE REQUIRED`, and will return a response of type [titan2.ClientCertRequiredResponse](#titan2clientcertrequiredresponse).
  * If *no valid response* can be returned, titan2 assigns a response type of "0" and returns a response of type [titan2.ErrorResponse](#titan2errorresponse).

  Parameters:
  * url: `string`
  * referer: `string` (optional)
  * timeout: `float` (optional)

  Returns: `[titan2.BaseResponse](#titan2baseresponse)`
  '''
  req = Request(url, cert_store=__cert_store, request_timeout=__timeout, referer=None)

  if timeout:
    req.set_timeout(timeout)

  return req.send()
