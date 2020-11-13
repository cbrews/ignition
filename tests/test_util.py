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

from titan2.util import normalize_path

class UtilTest(unittest.TestCase):
  def test_base_normalize_path(self):
    # Base test case
    self.assertEqual(normalize_path('/abc/def'), '/abc/def')

    # . test
    self.assertEqual(normalize_path('/abc/./def'), '/abc/def')

    # .. test
    self.assertEqual(normalize_path('/abc/../def'), '/def')

    # End . test
    self.assertEqual(normalize_path('/abc/def/.'), '/abc/def')

    # End .. test
    self.assertEqual(normalize_path('/abc/def/..'), '/abc')

    # Start . test
    self.assertEqual(normalize_path('./abc/def'), 'abc/def')

    # Start .. test
    self.assertEqual(normalize_path('../abc/def'), 'abc/def')

    # Complex string
    self.assertEqual(normalize_path('/a/b/c/./../../g'), '/a/g')

    # Weird base cases
    self.assertEqual(normalize_path(''), '')
    self.assertEqual(normalize_path('/'), '/')
