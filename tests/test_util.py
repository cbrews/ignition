'''
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one 
at http://mozilla.org/MPL/2.0/.
'''

import unittest

from ignition.util import normalize_path

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
