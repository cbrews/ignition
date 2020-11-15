'''
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one 
at http://mozilla.org/MPL/2.0/.
'''

import unittest

from ignition.request import Request

class RequestTests(unittest.TestCase):
  def setUp(self):
    self.request = Request(
      'software/',
      referer='gemini://gemini.circumlunar.space/',
      request_timeout=30
    )

  def test_set_timeout(self):
    self.request.set_timeout(10)
    self.assertEqual(self.request.timeout, 10)

  def test_get_url(self):
    self.assertEqual(
      self.request.get_url(),
      'gemini://gemini.circumlunar.space/software/'
    )

  def test_send(self):
    print("Requests.send() test skipped; it's currently too complex to test.")