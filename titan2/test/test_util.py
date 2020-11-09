import unittest
from ..util import normalize_path

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