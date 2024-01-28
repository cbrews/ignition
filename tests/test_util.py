"""
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one
at http://mozilla.org/MPL/2.0/.
"""

# pylint:disable=missing-function-docstring

from ignition.util import TimeoutManager, normalize_path


def test_base_normalize_path():
    # Base test case
    assert normalize_path("/abc/def") == "/abc/def"

    # . test
    assert normalize_path("/abc/./def") == "/abc/def"

    # .. test
    assert normalize_path("/abc/../def") == "/def"

    # End . test
    assert normalize_path("/abc/def/.") == "/abc/def"

    # End .. test
    assert normalize_path("/abc/def/..") == "/abc"

    # Start . test
    assert normalize_path("./abc/def") == "abc/def"

    # Start .. test
    assert normalize_path("../abc/def") == "abc/def"

    # Complex string
    assert normalize_path("/a/b/c/./../../g") == "/a/g"

    # Weird base cases
    assert normalize_path("") == ""
    assert normalize_path("/") == "/"


def test_timeout_manager():
    timeout_manager = TimeoutManager(10)

    # Handle initialization and override
    assert timeout_manager.get_timeout(None) == 10
    assert timeout_manager.get_timeout(20) == 20

    # Handle reset and override
    timeout_manager.set_default_timeout(12)

    assert timeout_manager.get_timeout(None) == 12
    assert timeout_manager.get_timeout(15) == 15
