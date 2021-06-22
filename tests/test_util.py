'''
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one
at http://mozilla.org/MPL/2.0/.
'''
# pylint:disable=missing-class-docstring,missing-function-docstring

from unittest import TestCase

from ignition.util import TimeoutManager, normalize_path


class UtilTest(TestCase):
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

  def test_timeout_manager(self):
    timeout_manager = TimeoutManager(10)

    # Handle initialization and override
    self.assertEqual(10, timeout_manager.get_timeout(None))
    self.assertEqual(20, timeout_manager.get_timeout(20))

    # Handle reset and override
    timeout_manager.set_default_timeout(12)

    self.assertEqual(12, timeout_manager.get_timeout(None))
    self.assertEqual(15, timeout_manager.get_timeout(15))
