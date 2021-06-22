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
    if component in ('.', ''):
      continue  # Do nothing
    if component == '..':
      if len(result_stack) > 0:
        result_stack.pop()
    else:
      result_stack.append(component)

  unescaped_path = ''.join([
    ('/' if len(path) > 0 and path[0] == '/' else ''),
    ('/'.join(result_stack)),
    ('/' if len(path) > 0 and path[len(path) - 1] == '/' else ''),
  ])

  return unescaped_path.replace("//", "/")


class TimeoutManager:
  '''
  Timeout Manager for global timeout management at the top-level
  '''
  def __init__(self, default_timeout):
    '''
    Sets a default timeout on initialization
    '''
    self.set_default_timeout(default_timeout)

  def set_default_timeout(self, default_timeout):
    '''
    Allow the default timeout to be overwritten
    '''
    self.default_timeout = default_timeout

  def get_timeout(self, timeout):
    '''
    Takes in a timeout and returns that, or the default timeout
    '''
    if timeout is not None:
      return timeout
    return self.default_timeout
