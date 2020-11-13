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
