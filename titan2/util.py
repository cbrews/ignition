import logging

logger = logging.getLogger(__name__)

def normalize_path(path):
  '''
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
