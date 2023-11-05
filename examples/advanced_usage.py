"""
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one
at http://mozilla.org/MPL/2.0/.
"""

import ignition

url = "//geminiprotocol.net/"
response = ignition.request(url)

if response.is_a(ignition.SuccessResponse):
    print("Success!")
    print(response.data())

elif response.is_a(ignition.InputResponse):
    print(f"Needs additional input: {response.data()}")

elif response.is_a(ignition.RedirectResponse):
    print(f"Received response, redirect to: {response.data()}")

elif response.is_a(ignition.TempFailureResponse):
    print(f"Error from server: {response.data()}")

elif response.is_a(ignition.PermFailureResponse):
    print(f"Error from server: {response.data()}")

elif response.is_a(ignition.ClientCertRequiredResponse):
    print(f"Client certificate required. {response.data()}")

elif response.is_a(ignition.ErrorResponse):
    print(f"There was an error on the request: {response.data()}")
