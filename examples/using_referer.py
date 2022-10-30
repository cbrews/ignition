"""
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one
at http://mozilla.org/MPL/2.0/.
"""

import ignition

response1 = ignition.request("//gemini.circumlunar.space")
response2 = ignition.request("software", referer=response1.url)

print(response2)
