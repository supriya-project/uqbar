#!/usr/bin/env python
import setuptools

description = 'Tools for building documentation with Sphinx, Graphviz and LaTeX'

classifiers = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: MacOS',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    ]

install_requires = [
    'Sphinx>=1.4.0',
    'cython',
    ]

keywords = [
    'sphinx',
    'graphviz',
    'latex',
    'documentation',
    ]

long_description = description

if __name__ == '__main__':
    setuptools.setup(
        author='Josiah Wolf Oberholtzer',
        author_email='josiah.oberholtzer@gmail.com',
        classifiers=classifiers,
        description=description,
        install_requires=install_requires,
        keywords=keywords,
        long_description=description,
        name='uqbar',
        packages=['uqbar'],
        url='https://github.com/josiah-wolf-oberholtzer/uqbar',
        version='0.1',
        zip_safe=False,
        )
