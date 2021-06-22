'''
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one
at http://mozilla.org/MPL/2.0/.
'''

import ignition

url = '//gemini.circumlunar.space'
response = ignition.request(url)

if response.is_a(ignition.SuccessResponse):
  print('Success!')
  print(response.data())

elif response.is_a(ignition.InputResponse):
  print('Needs additional input: %s' % (response.data()))

elif response.is_a(ignition.RedirectResponse):
  print('Received response, redirect to: %s' % (response.data()))

elif response.is_a(ignition.TempFailureResponse):
  print('Error from server: %s' % (response.data()))

elif response.is_a(ignition.PermFailureResponse):
  print('Error from server: %s' % (response.data()))

elif response.is_a(ignition.ClientCertRequiredResponse):
  print('Client certificate required. %s' % (response.data()))

elif response.is_a(ignition.ErrorResponse):
  print('There was an error on the request: %s' % (response.data()))
