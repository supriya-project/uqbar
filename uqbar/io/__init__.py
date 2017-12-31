"""
Tools for IO and file-system manipulation.
"""

import pathlib
import typing

from .DirectoryChange import DirectoryChange  # noqa
from .Profiler import Profiler  # noqa
from .RedirectedStreams import RedirectedStreams  # noqa
from .Timer import Timer  # noqa


def walk(
    root_path: typing.Union[str, pathlib.Path],
    top_down: bool=True,
    ) -> None:
    """
    Walks a directory tree.

    Like :py:func:`os.walk` but yielding instances of :py:class:`pathlib.Path`
    instead of strings.

    :param root_path: foo
    :param top_down: bar
    """
    root_path = pathlib.Path(root_path)
    directory_paths, file_paths = [], []
    for path in sorted(root_path.iterdir()):
        if path.is_dir():
            directory_paths.append(path)
        else:
            file_paths.append(path)
    if top_down:
        yield root_path, directory_paths, file_paths
    for directory_path in directory_paths:
        yield from walk(directory_path, top_down=top_down)
    if not top_down:
        yield root_path, directory_paths, file_paths


def write(
    contents: str,
    path: typing.Union[str, pathlib.Path],
    verbose: bool=False,
    ) -> None:
    """
    Writes ``contents`` to ``path``.

    Checks if ``path`` already exists and only write out new contents if the
    old contents do not match.

    Creates any intermediate missing directories.

    :param contents: the file contents to write
    :param path: the path to write to
    :param verbose: whether to print output
    """
    path = pathlib.Path(path)
    if path.exists():
        with path.open('r') as file_pointer:
            old_contents = file_pointer.read()
        if old_contents == contents:
            if verbose:
                print('preserved: {}'.format(path))
        else:
            with path.open('w') as file_pointer:
                file_pointer.write(contents)
            if verbose:
                print('rewrote: {}'.format(path))
    elif not path.exists():
        if not path.parent.exists():
            path.parent.mkdir(parents=True)
        with path.open('w') as file_pointer:
            file_pointer.write(contents)
        if verbose:
            print('wrote: {}'.format(path))
