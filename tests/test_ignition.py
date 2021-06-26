'''
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one
at http://mozilla.org/MPL/2.0/.
'''
# pylint:disable=missing-function-docstring,redefined-outer-name

import pytest

import ignition


@pytest.fixture
def request_mock(mocker):
  yield mocker.patch('ignition.Request')


def _destructure_request_args(request_mock):
  args, request_kwargs = request_mock.call_args
  request_url, = args
  return (
    request_url,
    request_kwargs['cert_store'],
    request_kwargs['request_timeout'],
    request_kwargs['referer'],
    request_kwargs['ca_cert']
  )


def test_request(request_mock):
  ignition.request('//test')

  request_mock.assert_called_once()

  request_url, cert_store, request_timeout, referer, ca_cert = _destructure_request_args(request_mock)

  assert request_url == '//test'
  assert cert_store.get_hosts_file() == ignition.DEFAULT_HOSTS_FILE
  assert request_timeout == ignition.DEFAULT_REQUEST_TIMEOUT
  assert referer is None
  assert ca_cert is None

  request_mock.return_value.send.assert_called_once()


def test_request_with_values(request_mock):

  ignition.request('path', referer='//test', timeout=10, ca_cert='string')

  request_mock.assert_called_once()

  request_url, cert_store, request_timeout, referer, ca_cert = _destructure_request_args(request_mock)

  assert request_url == 'path'
  assert cert_store.get_hosts_file() == ignition.DEFAULT_HOSTS_FILE
  assert request_timeout == 10
  assert referer == '//test'
  assert ca_cert == 'string'

  request_mock.return_value.send.assert_called_once()


def test_request_with_default_timeout(request_mock):

  ignition.set_default_timeout(9)
  ignition.request('//test')

  request_mock.assert_called_once()

  _, _, request_timeout, _, _, = _destructure_request_args(request_mock)

  assert request_timeout == 9

  request_mock.return_value.send.assert_called_once()


def test_request_with_overloaded_timeout(request_mock):

  ignition.set_default_timeout(8)
  ignition.request('//test', timeout=12)

  request_mock.assert_called_once()

  _, _, request_timeout, _, _, = _destructure_request_args(request_mock)

  assert request_timeout == 12

  request_mock.send_assert_called_once()


def test_request_with_hosts_file(request_mock):

  ignition.set_default_hosts_file('.my_hosts_file')
  ignition.request('//test')

  request_mock.assert_called_once()

  _, cert_store, _, _, _, = _destructure_request_args(request_mock)

  assert cert_store.get_hosts_file() == '.my_hosts_file'

  request_mock.return_value.send.assert_called_once()


def test_url(request_mock):
  ignition.url('//test')

  request_mock.assert_called_once_with('//test', referer=None)

  request_mock.return_value.get_url.assert_called_once()


def test_url_with_referer(request_mock):
  ignition.url('path', referer='//test')

  request_mock.assert_called_once_with('path', referer='//test')

  request_mock.return_value.get_url.assert_called_once()


def test_instance_objects():
  assert ignition.InputResponse is not None
  assert ignition.SuccessResponse is not None
  assert ignition.RedirectResponse is not None
  assert ignition.TempFailureResponse is not None
  assert ignition.PermFailureResponse is not None
  assert ignition.ClientCertRequiredResponse is not None
  assert ignition.ErrorResponse is not None


def test_constants():
  assert ignition.RESPONSE_STATUS_ERROR == "0"
  assert ignition.RESPONSE_STATUS_INPUT == "1"
  assert ignition.RESPONSE_STATUS_SUCCESS == "2"
  assert ignition.RESPONSE_STATUS_REDIRECT == "3"
  assert ignition.RESPONSE_STATUS_TEMP_FAILURE == "4"
  assert ignition.RESPONSE_STATUS_PERM_FAILURE == "5"
  assert ignition.RESPONSE_STATUS_CLIENTCERT_REQUIRED == "6"

  # Lighter test assertions on the details is fine
  assert ignition.RESPONSE_STATUSDETAIL_ERROR_NETWORK is not None
  assert ignition.RESPONSE_STATUSDETAIL_ERROR_DNS is not None
  assert ignition.RESPONSE_STATUSDETAIL_ERROR_HOST is not None
  assert ignition.RESPONSE_STATUSDETAIL_ERROR_TLS is not None
  assert ignition.RESPONSE_STATUSDETAIL_ERROR_PROTOCOL is not None
  assert ignition.RESPONSE_STATUSDETAIL_INPUT is not None
  assert ignition.RESPONSE_STATUSDETAIL_INPUT_SENSITIVE is not None
  assert ignition.RESPONSE_STATUSDETAIL_SUCCESS is not None
  assert ignition.RESPONSE_STATUSDETAIL_REDIRECT_TEMPORARY is not None
  assert ignition.RESPONSE_STATUSDETAIL_REDIRECT_PERMANENT is not None
  assert ignition.RESPONSE_STATUSDETAIL_TEMP_FAILURE is not None
  assert ignition.RESPONSE_STATUSDETAIL_TEMP_FAILURE_UNAVAILABLE is not None
  assert ignition.RESPONSE_STATUSDETAIL_TEMP_FAILURE_CGI is not None
  assert ignition.RESPONSE_STATUSDETAIL_TEMP_FAILURE_PROXY is not None
  assert ignition.RESPONSE_STATUSDETAIL_TEMP_FAILURE_SLOW_DOWN is not None
  assert ignition.RESPONSE_STATUSDETAIL_PERM_FAILURE is not None
  assert ignition.RESPONSE_STATUSDETAIL_PERM_FAILURE_NOT_FOUND is not None
  assert ignition.RESPONSE_STATUSDETAIL_PERM_FAILURE_GONE is not None
  assert ignition.RESPONSE_STATUSDETAIL_PERM_FAILURE_PROXY_REFUSED is not None
  assert ignition.RESPONSE_STATUSDETAIL_PERM_FAILURE_BAD_REQUEST is not None
  assert ignition.RESPONSE_STATUSDETAIL_CLIENTCERT_REQUIRED is not None
  assert ignition.RESPONSE_STATUSDETAIL_CLIENTCERT_REQUIRED_NOT_AUTHORIZED is not None
  assert ignition.RESPONSE_STATUSDETAIL_CLIENTCERT_REQUIRED_NOT_VALID is not None
