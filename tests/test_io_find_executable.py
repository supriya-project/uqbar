import platform
import sys
from pathlib import Path

import uqbar.io


def test_find_executable():
    print(f"{sys.executable=}")
    file_name = "python"
    if platform.system() == "Windows":
        file_name = "python.exe"
    found = uqbar.io.find_executable(file_name)
    sys_executable = str(Path(sys.executable).resolve())
    print(f"{sys_executable=}")
    print(f"{found=}")
    assert sys_executable in found
