'''
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one
at http://mozilla.org/MPL/2.0/.
'''
# pylint:disable=missing-class-docstring,missing-function-docstring

import datetime

import mock
import pytest

from ignition.exceptions import CertRecordParseException
from ignition.ssl.cert_record import CertRecord

test_datetime = datetime.datetime(2020, 11, 15, 12, 15, 2, 438000)
test_past_datetime = datetime.datetime(2018, 1, 1, 0, 0, 0, 0)


def test_initialize():
  cert_record = CertRecord('myhostname.sample', 'ssh-rsa fingerprint', test_datetime)
  assert cert_record.hostname == 'myhostname.sample'
  assert cert_record.fingerprint == 'ssh-rsa fingerprint'
  assert cert_record.expiration == test_datetime


def test_from_string():
  cert_record = CertRecord.from_string('myhostname.sample ssh-rsa fingerprint;EXPIRES=2020-11-15T12:15:02.438000\n')
  assert cert_record.hostname == 'myhostname.sample'
  assert cert_record.fingerprint == 'ssh-rsa fingerprint'
  assert cert_record.expiration == test_datetime


def test_from_string_invalid():
  with pytest.raises(CertRecordParseException):
    CertRecord.from_string('myhost.com\n')

  with pytest.raises(CertRecordParseException):
    CertRecord.from_string('myhost.com ssh-rsa fingerprint;EXPIRES=invalid\n')

  with pytest.raises(CertRecordParseException):
    CertRecord.from_string('\n')


def test_to_string():
  cert_record = CertRecord('myhostname.sample', 'ssh-rsa fingerprint', test_datetime)
  assert cert_record.to_string() == 'myhostname.sample ssh-rsa fingerprint;EXPIRES=2020-11-15T12:15:02.438000\n'


@mock.patch('ignition.ssl.cert_record.datetime')
def test_is_expired(datetime_mock):
  mocked_date_value = datetime.datetime(2020, 1, 1, 0, 0, 0, 0)
  datetime_mock.datetime.now = mock.Mock(return_value=mocked_date_value)

  cert_record_not_expired = CertRecord('myhostname.sample', 'ssh-rsa fingerprint', test_datetime)
  cert_record_expired = CertRecord('expired.sample', 'ssh-rsa fingerprint', test_past_datetime)

  assert cert_record_not_expired.now() == mocked_date_value
  assert cert_record_expired.now() == mocked_date_value
  assert not cert_record_not_expired.is_expired()
  assert cert_record_expired.is_expired()
