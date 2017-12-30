"""
Tools for IO and file-system manipulation.
"""

import pathlib


def walk(root_path, top_down=True):
    """
    Like :py:func:`os.walk` but yielding instances of :py:class:`pathlib.Path`
    instead of strings.
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


def write(contents, path, verbose=False):
    """
    Write ``contents`` to ``path``.

    Check if ``path`` already exists and only write out new
    contents if the old contents do not match.

    Create any intermediate missing directories.
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
