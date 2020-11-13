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

import unittest
import mock
import datetime

from titan2.cert_store import CertRecord

class CertRecordTests(unittest.TestCase):
  def setUp(self):
    self.test_datetime = datetime.datetime(2020, 11, 15, 12, 15, 2, 438000)
    self.test_past_datetime = datetime.datetime(2018, 1, 1, 0, 0, 0, 0)

  def test_initialize(self):
    cert_record = CertRecord('myhostname.sample', 'ssh-rsa fingerprint', self.test_datetime)
    self.assertEqual(cert_record.hostname, 'myhostname.sample')
    self.assertEqual(cert_record.fingerprint, 'ssh-rsa fingerprint')
    self.assertEqual(cert_record.expiration, self.test_datetime)

  def test_from_string(self):
    cert_record = CertRecord.from_string('myhostname.sample ssh-rsa fingerprint;EXPIRES=2020-11-15T12:15:02.438000')
    self.assertEqual(cert_record.hostname, 'myhostname.sample')
    self.assertEqual(cert_record.fingerprint, 'ssh-rsa fingerprint')
    self.assertEqual(cert_record.expiration, self.test_datetime)
    pass

  def test_to_string(self):
    cert_record = CertRecord('myhostname.sample', 'ssh-rsa fingerprint', self.test_datetime)
    self.assertEqual(
      cert_record.to_string(),
      'myhostname.sample ssh-rsa fingerprint;EXPIRES=2020-11-15T12:15:02.438000'
    )

  @mock.patch('titan2.cert_store.datetime')
  def test_is_expired(self, datetime_mock):
    mocked_date_value = datetime.datetime(2020, 1, 1, 0, 0, 0, 0)
    datetime_mock.datetime.now = mock.Mock(return_value=mocked_date_value)

    cert_record_not_expired = CertRecord('myhostname.sample', 'ssh-rsa fingerprint', self.test_datetime)
    cert_record_expired = CertRecord('expired.sample', 'ssh-rsa fingerprint', self.test_past_datetime)

    self.assertEqual(cert_record_not_expired.now(), mocked_date_value)
    self.assertEqual(cert_record_expired.now(), mocked_date_value)
    self.assertEqual(cert_record_not_expired.is_expired(), False)
    self.assertEqual(cert_record_expired.is_expired(), True)