'''
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one 
at http://mozilla.org/MPL/2.0/.
'''

import logging

logger = logging.getLogger(__name__)

def normalize_path(path: str) -> str:
  '''
  Implements a normalized path for a string
  See RFC-3986 https://tools.ietf.org/html/rfc3986#section-5.2.4
  5.2.4.  Remove Dot Segments

  Example:
    STEP   OUTPUT BUFFER         INPUT BUFFER

      1 :                         /a/b/c/./../../g
      2E:   /a                    /b/c/./../../g
      2E:   /a/b                  /c/./../../g
      2E:   /a/b/c                /./../../g
      2B:   /a/b/c                /../../g
      2C:   /a/b                  /../g
      2C:   /a                    /g
      2E:   /a/g
  '''
  result_stack = []
  for component in path.split('/'):
    if component == '.' or component == '':
      # Do nothing
      continue
    elif component == '..':
      if len(result_stack) > 0:
        result_stack.pop()
    else:
      result_stack.append(component)
  
  return (
    ('/' if len(path) > 0 and path[0] == '/' else '') + 
    ('/'.join(result_stack)) +
    ('/' if len(path) > 0 and path[len(path) - 1] == '/' else '')
  ).replace("//", "/")
