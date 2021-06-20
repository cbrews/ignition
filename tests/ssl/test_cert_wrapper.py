'''
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one
at http://mozilla.org/MPL/2.0/.
'''
# pylint:disable=missing-class-docstring,missing-function-docstring

import datetime
import unittest

from ignition.ssl.cert_wrapper import CertWrapper

from ..helpers import load_fixture_bytes


class CertWrapperTests(unittest.TestCase):
  def test_certificate_parse(self):
    cert_wrapper = CertWrapper.parse(load_fixture_bytes('sample_cert.der'))

    self.assertEqual(
      cert_wrapper.certificate.subject.rfc4514_string(),
      '1.2.840.113549.1.9.1=n/a,CN=n/a,OU=Test Certficate,O=Test Certificate,L=New York,ST=NY,C=US'
    )
    self.assertEqual(cert_wrapper.expiration(), datetime.datetime(2022, 2, 20, 17, 50, 54))
    self.assertEqual(
      cert_wrapper.fingerprint(),
      'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDzR2vptlPcQUlDHLanY9RsSwLgFHT3ecCyUicbY4HBOvlqRRL9l' +
      'dPQGFcblws0XsHcTNJABCe4xjPhzG4kFY/27hcgvnWiVX7gW1ylqWf6+dP7m+ewkU3xKK/XVmy0hBAIxuQoUhFzSA' +
      'zp+mx7lz3tm9OtOs2QFZu0U5FghVghSt6lUWJFDl2kWxzXxfscnCD9wFt5Plc9joxWF5xFBdx4Ocj/qpapdaiVoev' +
      'sGYNNK5wBisG0ejKPjmGo6MLQYMslRvwRajASMNVezDPddgrYsDLcCHCK0pijA2MMKnZZlIVRgin+DSVGaf4lYwPK' +
      'Wlf8Q6Ur6QRCn7MHaDkEFMAMvISkuQbaCJCTzZmWYKUxPolKWH+YoOC5YmhpVMJtR0naRqvJbGL21pWg8R4MXCjQM' +
      'ObHcMZEql5gEMxyJabWuS98HuCNaf3SzVQgpI3CI3PVxmHflZRwiwDuUWTXJ0UsFPelN1Vz0XVz8148wYUxGyABnI' +
      'RrAF0Z1htkb3iBFFo2R4MaPwLQtqNXQCdDlUXKHa4bVSQ6B7VBrL5KeDsFuvaWK+gQ9bfnqT+YSWGTVC2RyXtuvR+' +
      'Ee1JFqQckE+x2FGbbp5ZCPl1PdgQqPg5M+vXuLdnXk3T1R6ujQTMYL42gAUktHkApLcOQQ7wYFCB1KNXYxoNGsA0p' +
      'tMs0fsgcGQ=='
    )
