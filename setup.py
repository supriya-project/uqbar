#!/usr/bin/env python
import pathlib

import setuptools


def read_version():
    root_path = pathlib.Path(__file__).parent
    version_path = root_path / "uqbar" / "_version.py"
    with version_path.open() as file_pointer:
        file_contents = file_pointer.read()
    local_dict = {}
    exec(file_contents, None, local_dict)
    return local_dict["__version__"]


if __name__ == "__main__":
    setuptools.setup(
        package_data={"uqbar": ["py.typed"]},
        packages=setuptools.find_packages(
            include=["uqbar", "uqbar.*"], exclude=["*__pycache__*"]
        ),
        version=read_version(),
    )
