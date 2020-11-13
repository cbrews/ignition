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

from titan2.url import URL

class UrlBasicTests(unittest.TestCase):
  def test_standard_gemini_url(self):
    final_url = URL('gemini://gemini.circumlunar.space/')
    self.assertEqual(str(final_url), 'gemini://gemini.circumlunar.space/')
    self.assertEqual(final_url.protocol(), 'gemini://')
    self.assertEqual(final_url.host(), 'gemini.circumlunar.space')
    self.assertEqual(final_url.port(), 1965)
    self.assertEqual(final_url.path(), '/')
    self.assertEqual(final_url.query(), '')

  def test_url_without_scheme(self):
    final_url = URL('//gemini.circumlunar.space/')
    self.assertEqual(str(final_url), 'gemini://gemini.circumlunar.space/')
    self.assertEqual(final_url.protocol(), 'gemini://')
    self.assertEqual(final_url.host(), 'gemini.circumlunar.space')
    self.assertEqual(final_url.port(), 1965)
    self.assertEqual(final_url.path(), '/')
    self.assertEqual(final_url.query(), '')
  
  def test_url_with_different_scheme(self):
    final_url = URL('https://gemini.circumlunar.space/')
    self.assertEqual(str(final_url), 'https://gemini.circumlunar.space/')
    self.assertEqual(final_url.protocol(), 'https://')
    self.assertEqual(final_url.host(), 'gemini.circumlunar.space')
    self.assertEqual(final_url.port(), 1965)
    self.assertEqual(final_url.path(), '/')
    self.assertEqual(final_url.query(), '')

  def test_url_with_nonstandard_port(self):
    final_url = URL('gemini://gemini.circumlunar.space:80/')
    self.assertEqual(str(final_url), 'gemini://gemini.circumlunar.space:80/')
    self.assertEqual(final_url.protocol(), 'gemini://')
    self.assertEqual(final_url.host(), 'gemini.circumlunar.space')
    self.assertEqual(final_url.port(), 80)
    self.assertEqual(final_url.path(), '/')
    self.assertEqual(final_url.query(), '')

  def test_url_with_no_path(self):
    final_url = URL('gemini://gemini.circumlunar.space')
    self.assertEqual(str(final_url), 'gemini://gemini.circumlunar.space')
    self.assertEqual(final_url.protocol(), 'gemini://')
    self.assertEqual(final_url.host(), 'gemini.circumlunar.space')
    self.assertEqual(final_url.port(), 1965)
    self.assertEqual(final_url.path(), '')
    self.assertEqual(final_url.query(), '')

  def test_url_with_path(self):
    final_url = URL('gemini://gemini.circumlunar.space/test/path.gmi')
    self.assertEqual(str(final_url), 'gemini://gemini.circumlunar.space/test/path.gmi')
    self.assertEqual(final_url.protocol(), 'gemini://')
    self.assertEqual(final_url.host(), 'gemini.circumlunar.space')
    self.assertEqual(final_url.port(), 1965)
    self.assertEqual(final_url.path(), '/test/path.gmi')
    self.assertEqual(final_url.query(), '')

  def test_url_with_query(self):
    final_url = URL('gemini://gemini.circumlunar.space/test/path.gmi?user=name')
    self.assertEqual(str(final_url), 'gemini://gemini.circumlunar.space/test/path.gmi?user=name')
    self.assertEqual(final_url.protocol(), 'gemini://')
    self.assertEqual(final_url.host(), 'gemini.circumlunar.space')
    self.assertEqual(final_url.port(), 1965)
    self.assertEqual(final_url.path(), '/test/path.gmi')
    self.assertEqual(final_url.query(), 'user=name')

  def test_url_with_convoluted_path(self):
    final_url = URL('gemini://gemini.circumlunar.space/test/./test2/../path.gmi')
    self.assertEqual(str(final_url), 'gemini://gemini.circumlunar.space/test/path.gmi')
    self.assertEqual(final_url.protocol(), 'gemini://')
    self.assertEqual(final_url.host(), 'gemini.circumlunar.space')
    self.assertEqual(final_url.port(), 1965)
    self.assertEqual(final_url.path(), '/test/path.gmi')
    self.assertEqual(final_url.query(), '')
  
  # TODO - review
  def test_url_without_designation(self):
    final_url = URL('gemini.circumlunar.space/test')
    self.assertEqual(str(final_url), 'gemini://gemini.circumlunar.space/test')
    self.assertEqual(final_url.protocol(), 'gemini://')
    self.assertEqual(final_url.host(), '')
    self.assertEqual(final_url.port(), 1965)
    self.assertEqual(final_url.path(), 'gemini.circumlunar.space/test')
    self.assertEqual(final_url.query(), '')

class UrlRefererTests(unittest.TestCase):
  def test_standard_gemini_url(self):
    final_url = URL(
      'gemini://gus.guru/',
      referer_url='gemini://gemini.circumlunar.space/'
    )
    self.assertEqual(str(final_url), 'gemini://gus.guru/')
    self.assertEqual(final_url.protocol(), 'gemini://')
    self.assertEqual(final_url.host(), 'gus.guru')
    self.assertEqual(final_url.port(), 1965)
    self.assertEqual(final_url.path(), '/')
    self.assertEqual(final_url.query(), '')
  
  def test_url_without_scheme(self):
    final_url = URL(
      '//gus.guru/',
      referer_url='gemini://gemini.circumlunar.space/'
    )
    self.assertEqual(str(final_url), 'gemini://gus.guru/')
    self.assertEqual(final_url.protocol(), 'gemini://')
    self.assertEqual(final_url.host(), 'gus.guru')
    self.assertEqual(final_url.port(), 1965)
    self.assertEqual(final_url.path(), '/')
    self.assertEqual(final_url.query(), '')

  def test_absolute_path_url(self):
    final_url = URL(
      '/home',
      referer_url='gemini://gus.guru/search/page2'
    )
    self.assertEqual(str(final_url), 'gemini://gus.guru/home')
    self.assertEqual(final_url.protocol(), 'gemini://')
    self.assertEqual(final_url.host(), 'gus.guru')
    self.assertEqual(final_url.port(), 1965)
    self.assertEqual(final_url.path(), '/home')
    self.assertEqual(final_url.query(), '')

  def test_relative_path_url(self):
    final_url = URL(
      'page1',
      referer_url='gemini://gus.guru/search/page2'
    )
    self.assertEqual(str(final_url), 'gemini://gus.guru/search/page1')
    self.assertEqual(final_url.protocol(), 'gemini://')
    self.assertEqual(final_url.host(), 'gus.guru')
    self.assertEqual(final_url.port(), 1965)
    self.assertEqual(final_url.path(), '/search/page1')
    self.assertEqual(final_url.query(), '')

  def test_relative_path_url_with_trailing_slash(self):
    final_url = URL('page1/', referer_url='gemini://gus.guru/')
    self.assertEqual(str(final_url), 'gemini://gus.guru/page1/')
    self.assertEqual(final_url.protocol(), 'gemini://')
    self.assertEqual(final_url.host(), 'gus.guru')
    self.assertEqual(final_url.port(), 1965)
    self.assertEqual(final_url.path(), '/page1/')
    self.assertEqual(final_url.query(), '')
