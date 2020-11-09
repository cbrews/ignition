import cgi
import logging

from .globals import *

logger = logging.getLogger(__name__)

class ResponseFactory:
  @classmethod
  def create(self, url: str, status: str, meta=None, raw_body=None):
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

    factory_class = factories.get(basic_status_code, "0")
    return factory_class(url, status, meta, raw_body)

class BaseResponse:
  '''
  Response!
  '''

  def __init__(self, url, status, meta, raw_body):
    '''

    '''
    self.url = str(url)
    self.status = status
    self.meta = meta
    self.raw_body = raw_body

  def success(self):
    return isinstance(self, SuccessResponse)

  def data(self):
    return self.raw_body

  def __str__(self):
    return f"{self.status} {self.meta}"

class ErrorResponse(BaseResponse):
  def data(self):
    return self.meta

class InputResponse(BaseResponse):
  def data(self):
    return self.meta

class SuccessResponse(BaseResponse):
  '''

  '''
  def data(self):
    '''
    Decode the success message body using metadata
    '''

    meta = self.meta or GEMINI_DEFAULT_MIME_TYPE
    filetype, options = cgi.parse_header(meta)
    encoding = options['charset'] if 'charset' in options else GEMINI_DEFAULT_ENCODING
    try:
      return self.raw_body.decode(encoding)
    except LookupError:
      logger.warn(f"Could not decode response body using invalid encoding {encoding}")
      return self.raw_body
  
  def __str__(self):
    return f"{self.status} {self.meta}{CRLF}{self.data()}"

class RedirectResponse(BaseResponse):
  def data(self):
    return self.meta

class TempFailureResponse(BaseResponse):
  def data(self):
    return f"{self.status} {self.meta}"

class PermFailureResponse(BaseResponse):
  def data(self):
    return f"{self.status} {self.meta}"

class ClientCertRequiredResponse(BaseResponse):
  def data(self):
    return self.meta