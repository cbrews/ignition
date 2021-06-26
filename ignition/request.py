'''
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one
at http://mozilla.org/MPL/2.0/.
'''

import logging
import re
import socket
import ssl
from socket import gaierror as SocketGaiErrorException  # pylint:disable=no-name-in-module
from socket import herror as SocketHErrorException  # pylint:disable=no-name-in-module
from socket import timeout as SocketTimeoutException  # pylint:disable=no-name-in-module

import cryptography

from .exceptions import GeminiResponseParseError, RemoteCertificateExpired, TofuCertificateRejection
from .globals import *
from .response import BaseResponse, ResponseFactory
from .ssl.cert_wrapper import CertWrapper
from .url import URL

logger = logging.getLogger(__name__)


class Request:
  '''
  Handles a single request to a Gemini Server.

  The request handler has four key responsibilities:

  1. It manages resolution of the requested URL for
     the remote server, by invoking underlying URL parse
     logic
  2. It manages transmission of the request via TLS over a
     socket connection to the remote server.
  3. It validates SSL certificate response using a TOFU
     (trust-on-first-use) validation paradigm
  4. It manages raw response handling and designation to
     the Response object
  '''
  def __init__(self, url: str, referer=None, request_timeout=None, cert_store=None, ca_cert=None):
    '''
    Initializes Response with a url, referer, and timeout
    '''

    self.__url = URL(url, referer_url=referer)
    self.__timeout = request_timeout
    self.__cert_store = cert_store
    self.__ca_cert = ca_cert  # This should be a tuple

  def get_url(self):
    '''
    Fetch the generated URL for the request (based on referer, if present)
    '''

    return str(self.__url)

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
    if isinstance(secure_socket_result, BaseResponse):
      return secure_socket_result

    logger.debug(f"Validating server certificate to {self.__url.netloc()}")
    ssl_certificate_result = self.__validate_ssl_certificate(secure_socket_result)
    if isinstance(ssl_certificate_result, BaseResponse):
      return ssl_certificate_result

    logger.debug(f"Sending request header: {self.__url}")
    transport_result = self.__transport_payload(secure_socket_result, self.__url)
    if isinstance(transport_result, BaseResponse):
      return transport_result

    header, raw_body = transport_result
    logger.debug(f"Received response header: [{header}] and payload of length {len(raw_body)} bytes")
    return self.__handle_response(header, raw_body, ssl_certificate_result.certificate)

  def __get_socket(self):
    '''
    Creates a socket connection and manages exceptions.
    '''

    try:
      sock = socket.create_connection((self.__url.host(), self.__url.port()), timeout=self.__timeout)
      logger.debug(f"Created socket connection: {sock}")
      return sock
    except ConnectionRefusedError as err:
      logger.debug(f"ConnectionRefusedError: Connection to {self.__url.netloc()} was refused. {err}")
      return ResponseFactory.create(self.__url, RESPONSE_STATUSDETAIL_ERROR_HOST, "Connection refused")
    except ConnectionResetError as err:
      logger.debug(f"ConnectionResetError: Connection to {self.__url.netloc()} was reset. {err}")
      return ResponseFactory.create(self.__url, RESPONSE_STATUSDETAIL_ERROR_HOST, "Connection reset")
    except SocketHErrorException as err:
      logger.debug(f"socket.herror: socket.gethostbyaddr returned for {self.__url.host()}. {err}")
      return ResponseFactory.create(self.__url, RESPONSE_STATUSDETAIL_ERROR_HOST, "Host error")
    except SocketGaiErrorException as err:
      logger.debug(f"socket.gaierror: socket.getaddrinfo returned unknown host for {self.__url.host()}. {err}")
      return ResponseFactory.create(self.__url, RESPONSE_STATUSDETAIL_ERROR_DNS, "Unknown host")
    except SocketTimeoutException as err:
      logger.debug(f"socket.timeout: socket timed out connecting to {self.__url.host()}. {err}")
      return ResponseFactory.create(self.__url, RESPONSE_STATUSDETAIL_ERROR_HOST, "Socket timeout")
    except Exception as err:
      logger.error(f"Unknown exception encountered when connecting to {self.__url.netloc()} - {err}")
      raise err

  def __negotiate_ssl(self, socket_obj) -> ssl.SSLSocket:
    '''
    Negotiates a SSL handshake on the passed socket connection and returns the secure socket
    '''

    try:
      context = self.__setup_ssl_default_context()

      if self.is_using_ca_cert():
        self.__setup_ssl_client_certificate_context(context)

      secure_socket_result = context.wrap_socket(socket_obj, server_hostname=self.__url.host())
      return secure_socket_result
    except ssl.SSLError as err:
      logger.debug(f"ssl.SSLError for {self.__url.host()} - {err}")
      return ResponseFactory.create(self.__url, RESPONSE_STATUSDETAIL_ERROR_TLS, "Generic SSL Error")
    except ssl.SSLZeroReturnError as err:
      logger.debug(f"ssl.SSLZeroReturnError for {self.__url.host()} - {err}")
      return ResponseFactory.create(self.__url, RESPONSE_STATUSDETAIL_ERROR_TLS, "SSL Zero Return Error")
    except ssl.SSLWantReadError as err:
      logger.debug(f"ssl.SSLWantReadError for {self.__url.host()} - {err}")
      return ResponseFactory.create(self.__url, RESPONSE_STATUSDETAIL_ERROR_TLS, "SSL Read Error")
    except ssl.SSLWantWriteError as err:
      logger.debug(f"ssl.SSLWantWriteError for {self.__url.host()} - {err}")
      return ResponseFactory.create(self.__url, RESPONSE_STATUSDETAIL_ERROR_TLS, "SSL Write Error")
    except ssl.SSLSyscallError as err:
      logger.debug(f"ssl.SSLSyscallError for {self.__url.host()} - {err}")
      return ResponseFactory.create(self.__url, RESPONSE_STATUSDETAIL_ERROR_TLS, "SSL Syscall Error")
    except ssl.SSLEOFError as err:
      logger.debug(f"ssl.SSLEOFError for {self.__url.host()} - {err}")
      return ResponseFactory.create(self.__url, RESPONSE_STATUSDETAIL_ERROR_TLS, "SSL EOF Error")
    except ssl.SSLCertVerificationError as err:
      logger.debug(f"ssl.SSLCertVerificationError for {self.__url.host()} - {err}")
      return ResponseFactory.create(self.__url, RESPONSE_STATUSDETAIL_ERROR_TLS, "SSL Certificate Verification Error")
    except ssl.CertificateError as err:
      logger.debug(f"ssl.CertificateError for {self.__url.host()} - {err}")
      return ResponseFactory.create(self.__url, RESPONSE_STATUSDETAIL_ERROR_TLS, "SSL Certificate Error")
    except SocketTimeoutException:
      logger.debug(f"socket.timeout: socket timed out connecting to {self.__url.host()}")
      return ResponseFactory.create(self.__url, RESPONSE_STATUSDETAIL_ERROR_HOST, "Socket timeout")
    except Exception as err:
      logger.error(f"Unknown exception encountered when completing SSL handshake for {self.__url.host()} - {err}")
      raise err

  def __validate_ssl_certificate(self, secure_socket) -> CertWrapper:
    '''
    Trust-on-first-use (TOFU) validation on SSL certificate or throws exception
    '''

    try:
      certificate_wrapper = CertWrapper.parse(secure_socket.getpeercert(True))
      self.__cert_store.validate_tofu_or_add(secure_socket.server_hostname, certificate_wrapper)
      return certificate_wrapper
    except ValueError as err:
      logger.debug(f"ValueError: {self.__url.netloc()}. {err}")
      return ResponseFactory.create(self.__url, RESPONSE_STATUSDETAIL_ERROR_TLS, err)
    except RemoteCertificateExpired as err:
      logger.debug(f"RemoteCertificateExpired: {self.__url.netloc()} has an expired certificate. {err}")
      return ResponseFactory.create(self.__url, RESPONSE_STATUSDETAIL_ERROR_TLS, "Certificate expired")
    except TofuCertificateRejection as err:
      logger.debug(f"TofuCertificateRejection: {self.__url.netloc()} has an untrusted, unknown certificate. {err}")
      return ResponseFactory.create(self.__url, RESPONSE_STATUSDETAIL_ERROR_TLS, "Untrusted certificate (TOFU rejection)")
    except Exception as err:
      logger.error(f"Unknown exception encountered when validating ssl certificate on {self.__url.netloc()} - {err}")
      raise err

  def is_using_ca_cert(self):
    '''
    Returns if the request is using ca_cert
    '''
    return self.__ca_cert is not None

  def __setup_ssl_default_context(self):
    '''
    Setup an SSL default context (without a client certificate)
    This will bypass certificate validation against a CA.
    TOFU validation will be completed after the request is completed.
    '''

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context

  def __setup_ssl_client_certificate_context(self, context):
    '''
    Load cert chain for client certificate
    TODO: Better error handling here?
    '''
    cert, key = self.__ca_cert
    context.load_cert_chain(cert, key)

  def __transport_payload(self, socket_obj, payload):
    '''
    Handles Gemini protocol negotiation over the socket
    '''

    try:
      socket_obj.sendall((f"{payload}{CRLF}").encode(GEMINI_DEFAULT_ENCODING))
      fd = socket_obj.makefile('rb')
      return fd.readline().decode(GEMINI_DEFAULT_ENCODING).strip(), fd.read()
    except SocketTimeoutException:
      logger.debug(f"socket.timeout: socket timed out connecting to {self.__url.host()}")
      return ResponseFactory.create(self.__url, RESPONSE_STATUSDETAIL_ERROR_HOST, "Socket timeout")
    except Exception as err:
      logger.error(f"Unknown exception encountered when transporting data to {self.__url.netloc()} - {err}")
      raise err

  def __handle_response(self, header, raw_body, certificate: cryptography.x509.Certificate):
    '''
    Handles basic response data from the remote server and hands off to the Response object
    '''
    try:
      status, meta = re.split(GEMINI_RESPONSE_HEADER_SEPARATOR, header, maxsplit=1)

      if not re.match(r"^\d{2}$", status):
        raise GeminiResponseParseError("Response status is not a two-digit code")

      if len(meta) > GEMINI_RESPONSE_HEADER_META_MAXLENGTH:
        raise GeminiResponseParseError("Header meta text is too long")

      return ResponseFactory.create(self.__url, status, meta.strip(), raw_body, certificate)
    except GeminiResponseParseError as err:
      return ResponseFactory.create(self.__url, RESPONSE_STATUSDETAIL_ERROR_PROTOCOL, err)
