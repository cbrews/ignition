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

from titan2.request import Request

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