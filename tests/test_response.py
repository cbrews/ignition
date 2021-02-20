'''
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one 
at http://mozilla.org/MPL/2.0/.
'''

import unittest

from ignition.response import (
  ResponseFactory, 
  BaseResponse, 
  ErrorResponse, 
  InputResponse, 
  SuccessResponse, 
  RedirectResponse, 
  TempFailureResponse, 
  PermFailureResponse, 
  ClientCertRequiredResponse
)
from ignition.globals import (
  RESPONSE_STATUS_ERROR, 
  RESPONSE_STATUS_INPUT, 
  RESPONSE_STATUS_SUCCESS, 
  RESPONSE_STATUS_REDIRECT, 
  RESPONSE_STATUS_TEMP_FAILURE, 
  RESPONSE_STATUS_PERM_FAILURE, 
  RESPONSE_STATUS_CLIENTCERT_REQUIRED,
  RESPONSE_STATUSDETAIL_ERROR_NETWORK,
  RESPONSE_STATUSDETAIL_ERROR_DNS,
  RESPONSE_STATUSDETAIL_ERROR_HOST,
  RESPONSE_STATUSDETAIL_ERROR_TLS,
  RESPONSE_STATUSDETAIL_ERROR_PROTOCOL,
  RESPONSE_STATUSDETAIL_INPUT,
  RESPONSE_STATUSDETAIL_SUCCESS,
  RESPONSE_STATUSDETAIL_REDIRECT_TEMPORARY,
  RESPONSE_STATUSDETAIL_TEMP_FAILURE,
  RESPONSE_STATUSDETAIL_PERM_FAILURE,
  RESPONSE_STATUSDETAIL_CLIENTCERT_REQUIRED,
)

class ResponseFactoryTests(unittest.TestCase):
  def test_creates_input_response(self):
    response_object1 = ResponseFactory.create('url', '10', meta='Some input', raw_body=b'')
    response_object2 = ResponseFactory.create('url', '11', meta='', raw_body=b'')
    self.assertIsInstance(response_object1, InputResponse)
    self.assertIsInstance(response_object2, InputResponse)
  
  def test_creates_success_response(self):
    response_object = ResponseFactory.create('url', '20', meta='text/gemini', raw_body=b'Some body')
    self.assertIsInstance(response_object, SuccessResponse)
  
  def test_creates_redirect_response(self):
    response_object1 = ResponseFactory.create('url', '30', meta='', raw_body=b'')
    response_object2 = ResponseFactory.create('url', '31', meta='', raw_body=b'')
    self.assertIsInstance(response_object1, RedirectResponse)
    self.assertIsInstance(response_object2, RedirectResponse)
  
  def test_creates_temp_failure_response(self):
    response_object1 = ResponseFactory.create('url', '40', meta='', raw_body=b'')
    response_object2 = ResponseFactory.create('url', '44', meta='', raw_body=b'')
    self.assertIsInstance(response_object1, TempFailureResponse)
    self.assertIsInstance(response_object2, TempFailureResponse)
  
  def test_creates_perm_failure_response(self):
    response_object1 = ResponseFactory.create('url', '50', meta='', raw_body=b'')
    response_object2 = ResponseFactory.create('url', '57', meta='', raw_body=b'')
    self.assertIsInstance(response_object1, PermFailureResponse)
    self.assertIsInstance(response_object2, PermFailureResponse)

  def test_creates_client_cert_required_response(self):
    response_object1 = ResponseFactory.create('url', '60', meta='', raw_body=b'')
    response_object2 = ResponseFactory.create('url', '61', meta='', raw_body=b'')
    self.assertIsInstance(response_object1, ClientCertRequiredResponse)
    self.assertIsInstance(response_object2, ClientCertRequiredResponse)

  def test_creates_error_response(self):
    response_object1 = ResponseFactory.create('url', '01', meta='', raw_body=b'')
    response_object2 = ResponseFactory.create('url', '08', meta='', raw_body=b'')
    response_object3 = ResponseFactory.create('url', '99', meta='', raw_body=b'')
    response_object4 = ResponseFactory.create('url', 'ab', meta='', raw_body=b'')
    self.assertIsInstance(response_object1, ErrorResponse)
    self.assertIsInstance(response_object2, ErrorResponse)
    self.assertIsInstance(response_object3, ErrorResponse)
    self.assertIsInstance(response_object4, ErrorResponse)

class InputResponseTests(unittest.TestCase):
  '''
  Handles InputResponse type
  '''
  
  def setUp(self):
    self.response = ResponseFactory.create(
      'gemini://test.com/', 
      RESPONSE_STATUSDETAIL_INPUT, 
      meta='Enter a username',
      certificate='dummy cert object',
    )
  
  def test_url(self):
    self.assertEqual(self.response.url, 'gemini://test.com/')

  def test_basic_status(self):
    self.assertEqual(self.response.basic_status, RESPONSE_STATUS_INPUT)

  def test_status(self):
    self.assertEqual(self.response.status, RESPONSE_STATUSDETAIL_INPUT)

  def test_meta(self):
    self.assertEqual(self.response.meta, 'Enter a username')
  
  def test_raw_body(self):
    self.assertEqual(self.response.raw_body, None)

  def test_is_a(self):
    self.assertEqual(self.response.is_a(InputResponse), True)
    self.assertEqual(self.response.is_a(ErrorResponse), False)
    self.assertEqual(self.response.is_a(SuccessResponse), False)

  def test_success(self):
    self.assertEqual(self.response.success(), False)

  def test_data(self):
    self.assertEqual(self.response.data(), 'Enter a username')

  def test_certificate(self):
    self.assertEqual(self.response.certificate, 'dummy cert object')

class SuccessResponseTests(unittest.TestCase):
  '''
  Handles SuccessResponse type
  '''
  
  def setUp(self):
    self.response = ResponseFactory.create(
      'gemini://test.com/', 
      RESPONSE_STATUSDETAIL_SUCCESS, 
      meta='text/gemini; charset=utf-8',
      raw_body=b"This is a sample body\r\n\r\nHello",
      certificate='dummy cert object',
    )
  
  def test_url(self):
    self.assertEqual(self.response.url, 'gemini://test.com/')

  def test_basic_status(self):
    self.assertEqual(self.response.basic_status, RESPONSE_STATUS_SUCCESS)

  def test_status(self):
    self.assertEqual(self.response.status, RESPONSE_STATUSDETAIL_SUCCESS)

  def test_meta(self):
    self.assertEqual(self.response.meta, 'text/gemini; charset=utf-8')
  
  def test_raw_body(self):
    self.assertEqual(self.response.raw_body, b"This is a sample body\r\n\r\nHello")

  def test_is_a(self):
    self.assertEqual(self.response.is_a(SuccessResponse), True)
    self.assertEqual(self.response.is_a(ErrorResponse), False)

  def test_success(self):
    self.assertEqual(self.response.success(), True)

  def test_data(self):
    self.assertEqual(self.response.data(), 'This is a sample body\r\n\r\nHello')
  
  def test_certificate(self):
    self.assertEqual(self.response.certificate, 'dummy cert object')

class RedirectResponseTests(unittest.TestCase):
  '''
  Handles RedirectResponse type
  '''
  
  def setUp(self):
    self.response = ResponseFactory.create(
      'gemini://test.com/', 
      RESPONSE_STATUSDETAIL_REDIRECT_TEMPORARY,
      meta='gemini://test-new.com/',
      certificate='dummy cert object',
    )
  
  def test_url(self):
    self.assertEqual(self.response.url, 'gemini://test.com/')

  def test_basic_status(self):
    self.assertEqual(self.response.basic_status, RESPONSE_STATUS_REDIRECT)

  def test_status(self):
    self.assertEqual(self.response.status, RESPONSE_STATUSDETAIL_REDIRECT_TEMPORARY)

  def test_meta(self):
    self.assertEqual(self.response.meta, 'gemini://test-new.com/')
  
  def test_raw_body(self):
    self.assertEqual(self.response.raw_body, None)

  def test_is_a(self):
    self.assertEqual(self.response.is_a(RedirectResponse), True)
    self.assertEqual(self.response.is_a(ErrorResponse), False)
    self.assertEqual(self.response.is_a(SuccessResponse), False)

  def test_success(self):
    self.assertEqual(self.response.success(), False)

  def test_data(self):
    self.assertEqual(self.response.data(), 'gemini://test-new.com/')
  
  def test_certificate(self):
    self.assertEqual(self.response.certificate, 'dummy cert object')

class TempFailureResponseTests(unittest.TestCase):
  '''
  Handles TempFailureResponse type
  '''
  
  def setUp(self):
    self.response = ResponseFactory.create(
      'gemini://test.com/', 
      RESPONSE_STATUSDETAIL_TEMP_FAILURE, 
      meta='The server had trouble processing your response. Please try again.',
      certificate='dummy cert object',
    )
  
  def test_url(self):
    self.assertEqual(self.response.url, 'gemini://test.com/')

  def test_basic_status(self):
    self.assertEqual(self.response.basic_status, RESPONSE_STATUS_TEMP_FAILURE)

  def test_status(self):
    self.assertEqual(self.response.status, RESPONSE_STATUSDETAIL_TEMP_FAILURE)

  def test_meta(self):
    self.assertEqual(self.response.meta, 'The server had trouble processing your response. Please try again.')
  
  def test_raw_body(self):
    self.assertEqual(self.response.raw_body, None)

  def test_is_a(self):
    self.assertEqual(self.response.is_a(TempFailureResponse), True)
    self.assertEqual(self.response.is_a(ErrorResponse), False)
    self.assertEqual(self.response.is_a(SuccessResponse), False)

  def test_success(self):
    self.assertEqual(self.response.success(), False)

  def test_data(self):
    self.assertEqual(self.response.data(), '40 The server had trouble processing your response. Please try again.')
  
  def test_certificate(self):
    self.assertEqual(self.response.certificate, 'dummy cert object')

class PermFailureResponseTests(unittest.TestCase):
  '''
  Handles PermFailureResponse type
  '''
  
  def setUp(self):
    self.response = ResponseFactory.create(
      'gemini://test.com/', 
      RESPONSE_STATUSDETAIL_PERM_FAILURE, 
      meta='There was a permanent error on this page.',
      certificate='dummy cert object',
    )
  
  def test_url(self):
    self.assertEqual(self.response.url, 'gemini://test.com/')

  def test_basic_status(self):
    self.assertEqual(self.response.basic_status, RESPONSE_STATUS_PERM_FAILURE)

  def test_status(self):
    self.assertEqual(self.response.status, RESPONSE_STATUSDETAIL_PERM_FAILURE)

  def test_meta(self):
    self.assertEqual(self.response.meta, 'There was a permanent error on this page.')
  
  def test_raw_body(self):
    self.assertEqual(self.response.raw_body, None)

  def test_is_a(self):
    self.assertEqual(self.response.is_a(PermFailureResponse), True)
    self.assertEqual(self.response.is_a(ErrorResponse), False)
    self.assertEqual(self.response.is_a(SuccessResponse), False)

  def test_success(self):
    self.assertEqual(self.response.success(), False)

  def test_data(self):
    self.assertEqual(self.response.data(), '50 There was a permanent error on this page.')
  
  def test_certificate(self):
    self.assertEqual(self.response.certificate, 'dummy cert object')

class ClientCertRequiredResponseTests(unittest.TestCase):
  '''
  Handles ClientCertRequiredResponse type
  '''

  def setUp(self):
    self.response = ResponseFactory.create(
      'gemini://test.com/', 
      RESPONSE_STATUSDETAIL_CLIENTCERT_REQUIRED, 
      meta='Please create a client certificate for this request.',
      certificate='dummy cert object',
    )
  
  def test_url(self):
    self.assertEqual(self.response.url, 'gemini://test.com/')

  def test_basic_status(self):
    self.assertEqual(self.response.basic_status, RESPONSE_STATUS_CLIENTCERT_REQUIRED)

  def test_status(self):
    self.assertEqual(self.response.status, RESPONSE_STATUSDETAIL_CLIENTCERT_REQUIRED)

  def test_meta(self):
    self.assertEqual(self.response.meta, 'Please create a client certificate for this request.')
  
  def test_raw_body(self):
    self.assertEqual(self.response.raw_body, None)

  def test_is_a(self):
    self.assertEqual(self.response.is_a(ClientCertRequiredResponse), True)
    self.assertEqual(self.response.is_a(ErrorResponse), False)
    self.assertEqual(self.response.is_a(SuccessResponse), False)

  def test_success(self):
    self.assertEqual(self.response.success(), False)

  def test_data(self):
    self.assertEqual(self.response.data(), 'Please create a client certificate for this request.')
  
  def test_certificate(self):
    self.assertEqual(self.response.certificate, 'dummy cert object')

class ErrorResponseTests(unittest.TestCase):
  '''
  Handles ErrorResponse type
  '''

  def setUp(self):
    self.response = ResponseFactory.create(
      'gemini://test.com/', 
      RESPONSE_STATUSDETAIL_ERROR_DNS, 
      meta='Could not find a host at test.com.'
    )
  
  def test_url(self):
    self.assertEqual(self.response.url, 'gemini://test.com/')

  def test_basic_status(self):
    self.assertEqual(self.response.basic_status, RESPONSE_STATUS_ERROR)

  def test_status(self):
    self.assertEqual(self.response.status, RESPONSE_STATUSDETAIL_ERROR_DNS)

  def test_meta(self):
    self.assertEqual(self.response.meta, 'Could not find a host at test.com.')
  
  def test_raw_body(self):
    self.assertEqual(self.response.raw_body, None)

  def test_is_a(self):
    self.assertEqual(self.response.is_a(ErrorResponse), True)
    self.assertEqual(self.response.is_a(SuccessResponse), False)

  def test_success(self):
    self.assertEqual(self.response.success(), False)

  def test_data(self):
    self.assertEqual(self.response.data(), 'Could not find a host at test.com.')

  def test_certificate(self):
    self.assertEqual(self.response.certificate, None)

class ErrorResponseUnknownStatusTests(unittest.TestCase):
  '''
  Handles special ErrorResponse type for unmapped responses
  Note: other bad status responses (characters, not matching gemini scheme get caught upstream for now)
  '''

  def setUp(self):
    self.response = ResponseFactory.create(
      'gemini://test.com/',
      '99',
      meta='THIS IS A BAD RESPONSE'
    )
  
  def test_url(self):
    self.assertEqual(self.response.url, 'gemini://test.com/')

  def test_basic_status(self):
    self.assertEqual(self.response.basic_status, RESPONSE_STATUS_ERROR)

  def test_status(self):
    self.assertEqual(self.response.status, RESPONSE_STATUSDETAIL_ERROR_PROTOCOL)

  def test_meta(self):
    self.assertEqual(self.response.meta, 'Invalid response received from the server, status code: 99')
  
  def test_raw_body(self):
    self.assertEqual(self.response.raw_body, None)

  def test_is_a(self):
    self.assertEqual(self.response.is_a(ErrorResponse), True)
    self.assertEqual(self.response.is_a(SuccessResponse), False)

  def test_success(self):
    self.assertEqual(self.response.success(), False)

  def test_data(self):
    self.assertEqual(self.response.data(), 'Invalid response received from the server, status code: 99')

  def test_certificate(self):
    self.assertEqual(self.response.certificate, None)

class SuccessResponseAdvancedTests(unittest.TestCase):
  # TODO: More advanced tests around the success body response
  def test_default_metadata(self):
    pass

  def test_utf8_encoding(self):
    pass

  def test_other_encodings(self):
    pass