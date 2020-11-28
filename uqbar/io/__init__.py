"""
Tools for IO and file-system manipulation.
"""

import collections
import os
import pathlib
from typing import Generator, List, Optional, Sequence, Tuple, Union

from .DirectoryChange import DirectoryChange  # noqa
from .Profiler import Profiler  # noqa
from .RedirectedStreams import RedirectedStreams  # noqa
from .Timer import Timer  # noqa


def find_common_prefix(
    paths: Sequence[Union[str, pathlib.Path]]
) -> Optional[pathlib.Path]:
    """
    Find the common prefix of two or more paths.

    ::

        >>> import pathlib
        >>> one = pathlib.Path('foo/bar/baz')
        >>> two = pathlib.Path('foo/quux/biz')
        >>> three = pathlib.Path('foo/quux/wuux')

    ::

        >>> import uqbar.io
        >>> str(uqbar.io.find_common_prefix([one, two, three]))
        'foo'

    :param paths: paths to inspect
    """
    counter: collections.Counter = collections.Counter()
    for path in paths:
        path = pathlib.Path(path)
        counter.update([path])
        counter.update(path.parents)
    valid_paths = sorted(
        [path for path, count in counter.items() if count >= len(paths)],
        key=lambda x: len(x.parts),
    )
    if valid_paths:
        return valid_paths[-1]
    return None


def find_executable(name: str, flags=os.X_OK) -> List[str]:
    """
    Finds executable `name`.

    Similar to Unix ``which`` command.

    Returns list of zero or more full paths to `name`.
    """
    result = []
    extensions = [x for x in os.environ.get("PATHEXT", "").split(os.pathsep) if x]
    path = os.environ.get("PATH", None)
    if path is None:
        return []
    for path in os.environ.get("PATH", "").split(os.pathsep):
        path = os.path.join(path, name)
        if os.access(path, flags):
            result.append(path)
        for extension in extensions:
            path_extension = path + extension
            if os.access(path_extension, flags):
                result.append(path_extension)
    return result


def relative_to(
    source_path: Union[str, pathlib.Path], target_path: Union[str, pathlib.Path]
) -> pathlib.Path:
    """
    Generates relative path from ``source_path`` to ``target_path``.

    Handles the case of paths without a common prefix.

    ::

        >>> import pathlib
        >>> source = pathlib.Path('foo/bar/baz')
        >>> target = pathlib.Path('foo/quux/biz')

    ::

        >>> target.relative_to(source)
        Traceback (most recent call last):
          ...
        ValueError: 'foo/quux/biz' does not start with 'foo/bar/baz'

    ::

        >>> import uqbar.io
        >>> str(uqbar.io.relative_to(source, target))
        '../../quux/biz'

    :param source_path: the source path
    :param target_path: the target path
    """
    source_path = pathlib.Path(source_path).absolute()
    if source_path.is_file():
        source_path = source_path.parent
    target_path = pathlib.Path(target_path).absolute()
    common_prefix = find_common_prefix([source_path, target_path])
    if not common_prefix:
        raise ValueError("No common prefix")
    source_path = source_path.relative_to(common_prefix)
    target_path = target_path.relative_to(common_prefix)
    result = pathlib.Path(*[".."] * len(source_path.parts))
    return result / target_path


def walk(
    root_path: Union[str, pathlib.Path], top_down: bool = True
) -> Generator[
    Tuple[pathlib.Path, Sequence[pathlib.Path], Sequence[pathlib.Path]], None, None
]:
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
    path: Union[str, pathlib.Path],
    verbose: bool = False,
    logger_func=None,
) -> bool:
    """
    Writes ``contents`` to ``path``.

    Checks if ``path`` already exists and only write out new contents if the
    old contents do not match.

    Creates any intermediate missing directories.

    :param contents: the file contents to write
    :param path: the path to write to
    :param verbose: whether to print output
    """
    print_func = logger_func or print
    path = pathlib.Path(path)
    if path.exists():
        with path.open("r") as file_pointer:
            old_contents = file_pointer.read()
        if old_contents == contents:
            if verbose:
                print_func("preserved {}".format(path))
            return False
        else:
            with path.open("w") as file_pointer:
                file_pointer.write(contents)
            if verbose:
                print_func("rewrote {}".format(path))
            return True
    elif not path.exists():
        if not path.parent.exists():
            path.parent.mkdir(parents=True)
        with path.open("w") as file_pointer:
            file_pointer.write(contents)
        if verbose:
            print_func("wrote {}".format(path))
    return True
