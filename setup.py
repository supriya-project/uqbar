#!/usr/bin/env python
import pathlib
import setuptools


package_name = 'uqbar'


def read_version():
    root_path = pathlib.Path(__file__).parent
    version_path = root_path / package_name / '_version.py'
    with version_path.open() as file_pointer:
        file_contents = file_pointer.read()
    local_dict = {}
    exec(file_contents, None, local_dict)
    return local_dict['__version__']


description = 'Tools for building documentation with Sphinx, Graphviz and LaTeX'

classifiers = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: MacOS',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 3.6',
    ]

install_requires = [
    'Sphinx>=1.7.0',
    'Unidecode>=0.4.21',
    'sphinx-autodoc-typehints>=1.3.0',
    'sphinx-rtd-theme>=0.4.0',
    ]

keywords = [
    'sphinx',
    'graphviz',
    'latex',
    'documentation',
    ]

with open('README.md', 'r') as file_pointer:
    long_description = file_pointer.read()

version = read_version()

if __name__ == '__main__':
    setuptools.setup(
        author='Josiah Wolf Oberholtzer',
        author_email='josiah.oberholtzer@gmail.com',
        classifiers=classifiers,
        description=description,
        include_package_data=True,
        install_requires=install_requires,
        keywords=keywords,
        long_description=description,
        name=package_name,
        packages=[package_name],
        url='https://github.com/josiah-wolf-oberholtzer/uqbar',
        version=version,
        zip_safe=False,
        )
