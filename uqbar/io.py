"""
Tools for IO and file-system manipulation.
"""

import cProfile
import collections
import io
import os
import pathlib
import platform
import pstats
import subprocess
import sys
import time
from typing import Generator, List, Optional, Sequence, Tuple, Union


class DirectoryChange:
    """
    A context manager for temporarily changing the current working directory.

    This context manager is re-entrant.
    """

    ### INITIALIZER ###

    def __init__(self, directory, verbose=False):
        directory = pathlib.Path(directory).resolve().absolute()
        if not directory.is_dir():
            directory = directory.parent
        self._directory = directory
        self._directory_stack = []
        self._verbose = bool(verbose)

    ### SPECIAL METHODS ###

    def __enter__(self):
        if self.verbose:
            print("Changing directory to {} ...".format(self.directory))
        self._directory_stack.append(pathlib.Path.cwd())
        os.chdir(str(self._directory))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        original_directory = self._directory_stack.pop()
        if self.verbose:
            print("Returning to {} ...".format(original_directory))
        os.chdir(str(original_directory))

    ### PUBLIC PROPERTIES ###

    @property
    def directory(self):
        return self._directory

    @property
    def verbose(self):
        return self._verbose


class Profiler:
    """
    A context manager for profiling blocks of code.
    """

    def __enter__(self) -> "Profiler":
        self._profiler = cProfile.Profile()
        self._profiler.enable()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._profiler.disable()
        stream = io.StringIO()
        profiler_stats = pstats.Stats(self._profiler, stream=stream)
        profiler_stats = profiler_stats.sort_stats("cumulative")
        profiler_stats.print_stats()
        print(stream.getvalue())
        profiler_stats.dump_stats("stats.profile")


class RedirectedStreams:
    """
    A context manager for capturing ``stdout`` and ``stderr`` output.

    ..  container:: example

        ::

            >>> import uqbar.io
            >>> import io

        ::

            >>> string_io = io.StringIO()
            >>> with uqbar.io.RedirectedStreams(stdout=string_io):
            ...     print("hello, world!")
            ...

        ::

            >>> result = string_io.getvalue()
            >>> string_io.close()
            >>> print(result)
            hello, world!

    This context manager is not reentrant. Use a separate instance when nesting
    multiple timers.
    """

    ### INITIALIZER ###

    def __init__(self, stdout=None, stderr=None):
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr

    ### SPECIAL METHODS ###

    def __enter__(self):
        self._old_stdout, self._old_stderr = sys.stdout, sys.stderr
        self._old_stdout.flush()
        self._old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self._stdout.flush()
            self._stderr.flush()
        finally:
            sys.stdout = self._old_stdout
            sys.stderr = self._old_stderr

    ### PUBLIC PROPERTIES ###

    @property
    def stderr(self):
        return self._stderr

    @property
    def stdout(self):
        return self._stdout


class Timer:
    """
    A context manager for timing blocks of code.

    This context manager is not reentrant. Use a separate instance when nesting
    multiple timers.

    :param exit_message: message to print on entering the context
    :param enter_message: message to print on exiting the context
    :param verbose: whether to print output

    ::

        >>> import math
        >>> from uqbar.io import Timer
        >>> timer = Timer("Elapsed time:", "Looping!")
        >>> with timer:
        ...     for i in range(10000):
        ...         z = i ** math.pi
        ...
        Looping!
        Elapsed time: 0.0...

    """

    def __init__(
        self,
        exit_message: Optional[str] = None,
        enter_message: Optional[str] = None,
        verbose: bool = True,
    ) -> None:
        if enter_message is not None:
            enter_message = str(enter_message)
        self._enter_message = enter_message
        if exit_message is not None:
            exit_message = str(exit_message)
        self._exit_message = exit_message
        self._start_time: Optional[float] = None
        self._stop_time: Optional[float] = None
        self._verbose = bool(verbose)

    ### SPECIAL METHODS ###

    def __enter__(self) -> "Timer":
        if self.enter_message and self.verbose:
            print(self.enter_message)
        self._stop_time = None
        self._start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._stop_time = time.time()
        if self.exit_message and self.verbose:
            print(self.exit_message, self.elapsed_time)

    ### PUBLIC PROPERTIES ###

    @property
    def elapsed_time(self) -> Union[float, None]:
        if self.start_time is not None:
            if self.stop_time is not None:
                return self.stop_time - self.start_time
            return time.time() - self.start_time
        return None

    @property
    def enter_message(self) -> Union[str, None]:
        return self._enter_message

    @property
    def exit_message(self) -> Union[str, None]:
        return self._exit_message

    @property
    def start_time(self) -> Union[float, None]:
        return self._start_time

    @property
    def stop_time(self) -> Union[float, None]:
        return self._stop_time

    @property
    def verbose(self) -> bool:
        return self._verbose


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


def open_path(path: pathlib.Path) -> None:
    if platform.system() == "Darwin":
        subprocess.run(["open", str(path)], check=True)
    elif platform.system() == "Linux":
        subprocess.run(["xdg-open", str(path)], check=True)
    elif platform.system() == "Windows":
        os.startfile(str(path))  # type: ignore


def relative_to(
    source_path: Union[str, pathlib.Path], target_path: Union[str, pathlib.Path]
) -> pathlib.Path:
    """
    Generates relative path from ``source_path`` to ``target_path``.

    Handles the case of paths without a common prefix.

    ::

        >>> import os, pathlib
        >>> source = pathlib.Path('foo/bar/baz')
        >>> target = pathlib.Path('foo/quux/biz')

    ::

        >>> target.relative_to(source)
        Traceback (most recent call last):
          ...
        ValueError: ...

    ::

        >>> import uqbar.io
        >>> str(uqbar.io.relative_to(source, target)).replace(os.path.sep, "/")
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
    printed_path = str(path).replace(os.path.sep, "/")  # same display on Windows
    if path.exists():
        old_contents = path.read_text()
        if old_contents == contents:
            if verbose:
                print_func(f"preserved {printed_path}")
            return False
        else:
            path.write_text(contents)
            if verbose:
                print_func(f"rewrote {printed_path}")
            return True
    elif not path.exists():
        if not path.parent.exists():
            path.parent.mkdir(parents=True)
        path.write_text(contents)
        if verbose:
            print_func(f"wrote {printed_path}")
    return True
