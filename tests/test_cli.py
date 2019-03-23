import io

import pytest

import uqbar.cli
import uqbar.io
from uqbar.strings import normalize


class MeowCLI(uqbar.cli.CLI):

    alias = "meow"
    scripting_group = "mammals"
    short_description = "speak like a cat"

    def _process_args(self, arguments):
        if arguments.loud:
            print("MEOW!")
        else:
            print("Mew.")

    def _setup_argument_parser(self, parser):
        parser.add_argument("--loud", action="store_true", help="be adamant")


class SquawkCLI(uqbar.cli.CLI):

    alias = "squawk"
    scripting_group = "birds"
    short_description = "speak like a bird"

    def _process_args(self, arguments):
        if arguments.loud:
            print("CAW!")
        else:
            print("Cheap.")

    def _setup_argument_parser(self, parser):
        parser.add_argument("--loud", action="store_true", help="be adamant")


class WoofCLI(uqbar.cli.CLI):

    alias = "woof"
    scripting_group = "mammals"
    short_description = "speak like a dog"

    def _process_args(self, arguments):
        if arguments.loud:
            print("WOOF!")
        else:
            print("Wuf.")

    def _setup_argument_parser(self, parser):
        parser.add_argument("--loud", action="store_true", help="be adamant")


class VoxAggregator(uqbar.cli.CLIAggregator):
    @property
    def cli_classes(self):
        return [MeowCLI, SquawkCLI, WoofCLI]


def test_call():
    string_io = io.StringIO()
    with uqbar.io.RedirectedStreams(string_io, string_io):
        with pytest.raises(SystemExit):
            VoxAggregator()("mammals meow --loud")
    assert normalize(string_io.getvalue()) == normalize(
        """
        MEOW!
        """
    )


def test_call_help():
    string_io = io.StringIO()
    with uqbar.io.RedirectedStreams(string_io, string_io):
        with pytest.raises(SystemExit):
            VoxAggregator()("mammals meow --help")
    assert normalize(string_io.getvalue()) == normalize(
        """
        usage: meow-cli [-h] [--version] [--loud]

        speak like a cat

        optional arguments:
          -h, --help  show this help message and exit
          --version   show program's version number and exit
          --loud      be adamant
        """
    )


def test_help():
    string_io = io.StringIO()
    with uqbar.io.RedirectedStreams(string_io, string_io):
        with pytest.raises(SystemExit):
            VoxAggregator()("help")
    assert normalize(string_io.getvalue()) == normalize(
        """
        usage: vox-aggregator [-h] [--version] {help,list,birds,mammals} ...

        optional arguments:
          -h, --help            show this help message and exit
          --version             show program's version number and exit

        subcommands:
          {help,list,birds,mammals}
            help                print subcommand help
            list                list subcommands
            birds               {squawk} subcommand(s)
            mammals             {meow, woof} subcommand(s)
        """
    )


def test_list():
    string_io = io.StringIO()
    with uqbar.io.RedirectedStreams(string_io, string_io):
        with pytest.raises(SystemExit):
            VoxAggregator()("list")
    assert normalize(string_io.getvalue()) == normalize(
        """
        [birds]
            squawk: speak like a bird

        [mammals]
            meow: speak like a cat
            woof: speak like a dog
        """
    )
