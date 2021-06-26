'''
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one
at http://mozilla.org/MPL/2.0/.
'''
# pylint:disable=missing-function-docstring

from ignition.request import Request

request = Request('software/', referer='gemini://gemini.circumlunar.space/', request_timeout=30)


def test_get_url():
  assert request.get_url() == 'gemini://gemini.circumlunar.space/software/'


def test_send():
  print("Requests.send() test skipped; it's currently too complex to test.")
