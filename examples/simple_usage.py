"""
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one
at http://mozilla.org/MPL/2.0/.
"""

import ignition

# Fetch capsule content
response = ignition.request("//gemini.circumlunar.space")

# Get status from remote capsule
print(response.status)

# Get response information from remote capsule
print(response.data())
