import abc
import argparse
import os
import pathlib
import typing
import uqbar.strings
from configparser import ConfigParser


class CLI(abc.ABC):
    '''
    Abstract base for CLI scripts.
    '''

    ### CLASS VARIABLES ###

    _colors = {
        'BLUE': '\033[94m',
        'RED': '\033[91m',
        'GREEN': '\033[92m',
        'END': '\033[0m',
        }

    config_name: str = '.uqbarrc'
    long_description: typing.Optional[str] = None
    short_description: typing.Optional[str] = None
    version: float = 1.0

    ### INITIALIZER ###

    def __init__(self):
        short_description = getattr(self, 'short_description', None)
        long_description = getattr(self, 'long_description', None)
        if long_description:
            long_description = uqbar.strings.normalize(long_description)
        parser = self._argument_parser = argparse.ArgumentParser(
            description=short_description,
            epilog=long_description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            prog=self.program_name,
            )
        version = '%(prog)s {}'
        version = version.format(getattr(self, 'version', 1.0))
        parser.add_argument('--version', action='version', version=version)
        self._argument_parser = parser
        self._setup_argument_parser(parser)
        self._config_parser = None

    ### SPECIAL METHODS ###

    def __call__(self, arguments=None) -> None:
        r'''Calls developer script.

        Returns none.
        '''
        self._config_parser = self._read_config_files()
        if arguments is None:
            arguments = self.argument_parser.parse_args()
        else:
            if isinstance(arguments, str):
                arguments = arguments.split()
            elif not isinstance(arguments, (list, tuple)):
                raise ValueError
            arguments = self.argument_parser.parse_args(arguments)
        self._process_args(arguments)

    ### PRIVATE METHODS ###

    def _is_valid_path(self, path) -> bool:
        path = pathlib.Path(path)
        return path.exists() and path.is_dir()

    @abc.abstractmethod
    def _process_args(self, arguments):
        raise NotImplementedError

    def _read_config_files(self) -> ConfigParser:
        paths = []
        home_config = pathlib.Path().home() / self.config_name
        if home_config.exists():
            paths.append(home_config)
        path = pathlib.Path.cwd()
        while not path.joinpath(self.config_name).exists():
            path = path.parent
            if path.parent == path:
                break
        if path.joinpath(self.config_name).exists():
            if path.joinpath(self.config_name) not in paths:
                paths.append(path.joinpath(self.config_name))
        config_parser = ConfigParser()
        config_parser.read([str(_) for _ in paths])
        return config_parser

    @abc.abstractmethod
    def _setup_argument_parser(self, parser: argparse.ArgumentParser):
        raise NotImplementedError

    def _validate_path(self, path):
        message = '{!r} is not a valid directory.'
        message = message.format(path)
        error = argparse.ArgumentTypeError(message)
        path = os.path.abspath(path)
        if not self._is_valid_path(path):
            raise error
        return os.path.relpath(path)

    ### PUBLIC PROPERTIES ###

    @property
    def argument_parser(self):
        r'''The script's instance of argparse.ArgumentParser.
        '''
        return self._argument_parser

    @property
    def formatted_help(self):
        r'''Formatted help of developer script.
        '''
        return self._argument_parser.format_help()

    @property
    def formatted_usage(self):
        r'''Formatted usage of developer script.
        '''
        return self._argument_parser.format_usage()

    @property
    def formatted_version(self):
        r'''Formatted version of developer script.
        '''
        return self._argument_parser.format_version()

    @property
    def program_name(self):
        r'''The name of the script, callable from the command line.
        '''
        name = '-'.join(
            word.lower() for word in
            uqbar.strings.delimit_words(type(self).__name__)
            )
        return name
