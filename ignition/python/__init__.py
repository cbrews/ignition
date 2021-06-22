'''
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one 
at http://mozilla.org/MPL/2.0/.
'''

import sys

# Polyfill to include gemini in urllib parsing
if sys.version_info > (3, 10):
  raise Exception("Python versions > 3.9.x are not supported at this time.")

if sys.version_info > (3, 9):
  from .python3_9.Lib import urllib
elif sys.version_info > (3, 8):
  from .python3_8.Lib import urllib
elif sys.version_info > (3, 7):
  from .python3_7.Lib import urllib
else:
  raise Exception("Python versions < 3.7 are not supported at this time.")
