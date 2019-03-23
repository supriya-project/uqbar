import sys

import uqbar.io


def test_find_executable():
    found = uqbar.io.find_executable("python")
    assert any(sys.executable.startswith(_) for _ in found)
