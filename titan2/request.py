import socket
import re
import ssl
import logging

from .globals import *
from .response import BaseResponse, ResponseFactory
from .url import URL

logger = logging.getLogger(__name__)

class Request:
  '''
  Handles a single request to a Gemini Server.

  The request handler has three key responsibilities:

  1. It manages resolution of the requested URL for
     the remote server, by invoking underlying URL parse
     logic
  2. It manages transmission of the request via TLS over a
     socket connection to the remote server.
  3. It manages raw response handling and designation to 
     the Response object
  '''

  def __init__(self, url: str, referer=None, timeout=None):
    '''
    Initializes Response with a url, referer, and timeout
    '''

    self.__url = URL(url, referer_url=referer)
    self.timeout = timeout if timeout else REQUEST_DEFAULT_TIMEOUT

  def send(self):
    '''
    Performes network communication and returns a Response object
    '''

    logger.debug(f"Attempting to create a connection to {self.__url.netloc()}")
    socket_result = self.__get_socket()
    if isinstance(socket_result, BaseResponse):
      return socket_result

    logger.debug(f"Attempting to negotiate SSL handshake with {self.__url.netloc()}")
    secure_socket_result = self.__negotiate_ssl(socket_result)
    if isinstance(socket_result, BaseResponse):
      return secure_socket_result

    logger.debug(f"Sending request header: {self.__url}")
    header, raw_body = self.__transport_payload(secure_socket_result, self.__url)

    logger.debug(f"Received response header: [{header}] and payload of length {len(raw_body)} bytes")
    return self.__handle_response(header, raw_body)
  
  def url(self):
    return str(self.__url)

  def __get_socket(self):
    '''
    Creates a socket connection and manages exceptions.
    '''

    try:
      sock = socket.create_connection((self.__url.host(), self.__url.port()))
      sock.settimeout(self.timeout)
      logger.debug(f"Created socket connection: {sock}")
      return sock
    except ConnectionRefusedError as err:
      logger.debug(f"ConnectionRefusedError: Connection to {self.__url.netloc()} was refused. {err}")
      return ResponseFactory.create(self.__url, RESPONSE_STATUSDETAIL_ERROR_REFUSED, "Connection refused")
    except ConnectionResetError as err:
      logger.debug(f"ConnectionResetError: Connection to {self.__url.netloc()} was reset. {err}")
      return ResponseFactory.create(self.__url, RESPONSE_STATUSDETAIL_ERROR_RESET, "Connection reset")
    except socket.herror as err:
      logger.debug(f"socket.herror: socket.gethostbyaddr returned for {self.__url.host()}. {err}")
      return ResponseFactory.create(self.__url, RESPONSE_STATUSDETAIL_ERROR_HOST_ERROR, "Host error")
    except socket.gaierror as err:
      logger.debug(f"socket.gaierror: socket.getaddrinfo returned unknown host for {self.__url.host()}.  {err}")
      return ResponseFactory.create(self.__url, RESPONSE_STATUSDETAIL_ERROR_UNKNOWN_HOST, "Unknown host")
    except socket.timeout as err:
      logger.debug(f"socket.timeout: socket timed out connecting to {self.__url.host()}. {err}")
      return ResponseFactory.create(self.__url, RESPONSE_STATUSDETAIL_ERROR_TIMEOUT, "Socket timeout")
    except Exception as err:
      logger.error(f"Unknown exception encountered when connecting to {self.__url.netloc()} - {err}")
      raise err

  def __negotiate_ssl(self, socket, cafile=None):
    '''
    Negotiates a SSL handshake on the passed socket connection and returns the secure socket
    '''

    try:
      context = ssl.create_default_context()
      context.check_hostname = False
      context.verify_mode = ssl.CERT_NONE
      return context.wrap_socket(socket, server_hostname=self.__url.host())
    except ssl.SSLError as err:
      logger.error(f"ssl.SSLError for {self.__url.host()} - {err}")
      raise err
    except ssl.SSLZeroReturnError as err:
      logger.error(f"ssl.SSLZeroReturnError for {self.__url.host()} - {err}")
      raise err
    except ssl.SSLWantReadError as err:
      logger.error(f"ssl.SSLWantReadError for {self.__url.host()} - {err}")
      raise err
    except ssl.SSLWantWriteError as err:
      logger.error(f"ssl.SSLWantWriteError for {self.__url.host()} - {err}")
      raise err
    except ssl.SSLSyscallError as err:
      logger.error(f"ssl.SSLSyscallError for {self.__url.host()} - {err}")
      raise err
    except ssl.SSLEOFError as err:
      logger.error(f"ssl.SSLEOFError for {self.__url.host()} - {err}")
      raise err
    except ssl.SSLCertVerificationError as err:
      logger.error(f"ssl.SSLCertVerificationError for {self.__url.host()} - {err}")
      raise err
    except ssl.CertificateError as err:
      logger.error(f"ssl.CertificateError for {self.__url.host()} - {err}")
      raise err
    except Exception as err:
      logger.error(f"Unknown exception encountered when completing SSL handshake for {self.__url.host()} - {err}")
      raise err
    else:
      return None

  def __transport_payload(self, socket, payload):
    '''
    Handles Gemini protocol negotiation over the socket
    '''

    try:
      socket.sendall((f"{payload}{CRLF}").encode(GEMINI_DEFAULT_ENCODING))
      fd = socket.makefile('rb')
      return fd.readline().decode(GEMINI_DEFAULT_ENCODING).strip(), fd.read()
    except Exception as err:
      logger.error(f"Unknown exception encountered when transporting data to {self.__url.netloc()} - {err}")
      raise err

  def __handle_response(self, header, raw_body):
    '''
    Handles basic response data from the remote server and hands off to the Response object
    '''

    status, meta = header.split(GEMINI_RESPONSE_HEADER_SEPARATOR, maxsplit=1)

    if not re.match(r"^\d{2}$", status) or len(meta) > GEMINI_RESPONSE_HEADER_META_MAXLENGTH:
      return ResponseFactory.create(
        self.__url,
        RESPONSE_STATUSDETAIL_ERROR_BAD_RESPONSE,
        "Bad response header from server"
      )

    return ResponseFactory.create(
      self.__url,
      status, 
      meta.strip(),
      raw_body
    )