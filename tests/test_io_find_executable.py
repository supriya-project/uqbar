import platform
import sys

import uqbar.io


def test_find_executable():
    file_name = "python"
    if platform.system() == "Windows":
        file_name = "python.exe"
    found = uqbar.io.find_executable(file_name)
    print(found)
    print(sys.executable)
    assert any(sys.executable.startswith(_) for _ in found)
