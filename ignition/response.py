'''
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one
at http://mozilla.org/MPL/2.0/.
'''

import cgi
import logging

from cryptography.x509 import Certificate

from .globals import *

logger = logging.getLogger(__name__)


class ResponseFactory:
  '''
  Wrapper class for factory:
  Determines the approriate response type based on response status
  and generates the appropriate response type
  '''
  @classmethod
  def create(cls, url: str, status: str, meta=None, raw_body=None, certificate=None):
    '''
    Given a url, status, and response data, generates the appropriate response type
    '''
    basic_status_code = status[0]
    factories = {
      "0": ErrorResponse,
      "1": InputResponse,
      "2": SuccessResponse,
      "3": RedirectResponse,
      "4": TempFailureResponse,
      "5": PermFailureResponse,
      "6": ClientCertRequiredResponse,
    }

    factory_class = factories.get(basic_status_code, None)

    if factory_class is None:
      return ErrorResponse(
        url,
        RESPONSE_STATUSDETAIL_ERROR_PROTOCOL,
        f"Invalid response received from the server, status code: {status}",
        None,
        None,
      )

    return factory_class(url, status, meta, raw_body, certificate)


class BaseResponse:
  '''
  Abstract Base response type that all response types inherit from.
  Included public members:
  * url
  * basic_status
  * status
  * meta
  * raw_body
  * certificate
  '''

  url: str
  basic_status: str
  status: str
  meta: str
  raw_body: bytes
  certificate: Certificate

  def __init__(self, url: str, status: str, meta: str, raw_body: bytes, certificate: Certificate):
    '''
    Initializes a BaseResponse with the request url, status code, metadata, raw body string, and remote certificate
    '''
    self.url = str(url)
    self.basic_status = status[0]
    self.status = status
    self.meta = meta
    self.raw_body = raw_body
    self.certificate = certificate

  def is_a(self, response_class_type):
    '''
    Returns true if the response class type matches the current class
    '''
    return isinstance(self, response_class_type)

  def success(self):
    '''
    Returns true if the response is of the type success
    '''
    return self.is_a(SuccessResponse)

  def data(self):
    '''
    Fetches processed data from the response.  This method should be overloaded in each specific response type.
    '''
    return self.raw_body

  def __str__(self):
    '''
    Returns a literal string representation of the response, including messageheader
    '''
    return f"{self.status} {self.meta}"

  def __repr__(self):
    '''
    A representation of the string for developers
    '''
    return f'<ignition.response.{self.__class__.__name__}: {self.status} {self.meta} [from {self.url}]>'


class ErrorResponse(BaseResponse):
  '''
  ErrorResponse
  This is a custom response type for ignition, to handle any responses representing request errors
  that are outside of the scope of the Gemini protocol.  Included options are:

  00: RESPONSE_STATUSDETAIL_ERROR_NETWORK
  Any errors that occur at the network level, and prevented the client from making any connection
  with external services.

  01: RESPONSE_STATUSDETAIL_ERROR_DNS = "01"
  Any errors at the DNS level.

  02: RESPONSE_STATUSDETAIL_ERROR_HOST
  Any errors connecting to the host (timeout, refused, etc.).

  03: RESPONSE_STATUSDETAIL_ERROR_TLS
  Any errors associated with TLS/SSL, including handshake errors, certificate expired errors,
  and security errors like certificate rejection errors.

  04: RESPONSE_STATUSDETAIL_ERROR_PROTOCOL
  Any errors where a secure message is received from the server, but it does not conform to the
  Gemini protocol requirements and cannot be processed.
  '''
  def data(self):
    '''
    Fetch data relevant to the ErrorResponse; in this case the metadata message from the response
    '''
    return self.meta


class InputResponse(BaseResponse):
  '''
  InputRequest
  Meets Gemini specification: 3.2.1 1x (INPUT)

  Status codes beginning with 1 are INPUT status codes, meaning that
  the requested resource accepts a line of textual user input.

  The user should reissue a request to the url with parameters in the form:
  gemini://hostname/path?query
  '''
  def data(self):
    '''
    Returns the related instructions for the InputResponse.
    The <META> line is a prompt which should be displayed to the user.
    '''
    return self.meta


class SuccessResponse(BaseResponse):
  '''
  SuccessResponse
  Meets Gemini specification: 3.2.2 2x (SUCCESS)

  Status codes beginning with 2 are SUCCESS status codes.
  '''
  def data(self):
    '''
    Decode the success message body using metadata in the appropriate encoding type
    '''

    meta = self.meta or GEMINI_DEFAULT_MIME_TYPE
    _, options = cgi.parse_header(meta)
    encoding = options['charset'] if 'charset' in options else GEMINI_DEFAULT_ENCODING
    try:
      return self.raw_body.decode(encoding)
    except LookupError:
      logger.warning(f"Could not decode response body using invalid encoding {encoding}")
      return self.raw_body
    except UnicodeDecodeError:
      logger.warning(f"Could not decode response body via encoding {encoding}, returning raw data")
      return self.raw_body

  def __str__(self):
    '''
    The string representation of the success message should be header + body
    '''
    return f"{self.status} {self.meta}{CRLF}{self.data()}"


class RedirectResponse(BaseResponse):
  '''
  RedirectResponse
  Meets Gemini specification: 3.2.3 3x (REDIRECT)

  Status codes beginning with 3 are REDIRECT status codes.

  The server is redirecting the client to a new location for the requested resource
  '''
  def data(self):
    '''
    Returns the new destination for redirection from the server
    '''
    return self.meta


class TempFailureResponse(BaseResponse):
  '''
  TempFailureResponse
  Meets Gemini specification: 3.2.4 4x (TEMPORARY FAILURE)

  Status codes beginning with 4 are TEMPORARY FAILURE status codes.

  The request has failed, but an identical request may success in the future.
  '''
  def data(self):
    '''
    Returns the data from the server in the META field, which may provide additional information to the user.
    '''
    return f"{self.status} {self.meta}"


class PermFailureResponse(BaseResponse):
  '''
  PermFailureResponse
  Meets Gemini specification: 3.2.5 5x (PERMANENT FAILURE)

  Status codes beginning with 5 are PERMANENT FAILURE status codes.

  The request has failed, identical requests will likely fail in the future.
  '''
  def data(self):
    '''
    Returns the data from the server in the META field, which may provide additional information to the user.
    '''
    return f"{self.status} {self.meta}"


class ClientCertRequiredResponse(BaseResponse):
  '''
  ClientCertRequiredResponse
  Meets Gemini specification: 3.2.6 6x (CLIENT CERTIFICATE REQUIRED)

  Status codes beginning with 6 are CLIENT CERTIFICATE REQUIRED status codes

  The request should be retried with a client certificate.
  '''
  def data(self):
    '''
    Return additional information from the server on certificate requirements
    or the reason a certificate was rejected
    '''
    return self.meta
