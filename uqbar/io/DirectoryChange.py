import os
import pathlib


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
            print('Changing directory to {} ...'.format(self.directory))
        self._directory_stack.append(pathlib.Path.cwd())
        os.chdir(str(self._directory))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        original_directory = self._directory_stack.pop()
        if self.verbose:
            print('Returning to {} ...'.format(original_directory))
        os.chdir(str(original_directory))

    ### PUBLIC PROPERTIES ###

    @property
    def directory(self):
        return self._directory

    @property
    def verbose(self):
        return self._verbose
