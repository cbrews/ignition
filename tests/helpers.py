'''
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one 
at http://mozilla.org/MPL/2.0/.
'''

import os


def load_fixture_bytes(filename: str) -> bytes:
  '''
  Load a fixture as bytes
  '''
  fixture_path = os.path.join(os.path.dirname(__file__), './fixtures', filename)
  with open(fixture_path, 'rb') as fixture_handler:
    return fixture_handler.read()