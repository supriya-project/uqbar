import abc
import sys

from uqbar.cli.CLI import CLI


class CLIAggregator(CLI):
    """
    Aggregates CLI scripts.

    ::

        >>> import uqbar.cli
        >>> class ExampleAggregator(uqbar.cli.CLIAggregator):
        ...     @property
        ...     def cli_classes(self):
        ...         return []
        ...
        >>> script = ExampleAggregator()
        >>> try:
        ...     script('--help')
        ... except SystemExit:
        ...     pass
        ...
        usage: example-aggregator [-h] [--version] {help,list} ...
        <BLANKLINE>
        optional arguments:
          -h, --help   show this help message and exit
          --version    show program's version number and exit
        <BLANKLINE>
        subcommands:
          {help,list}
            help       print subcommand help
            list       list subcommands

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(self, arguments=None):
        if arguments is None:
            arguments = self.argument_parser.parse_known_args()
        else:
            if isinstance(arguments, str):
                arguments = arguments.split()
            elif not isinstance(arguments, (list, tuple)):
                message = "must be str, list, tuple or none: {!r}."
                message = message.format(arguments)
                raise ValueError(message)
            arguments = self.argument_parser.parse_known_args(arguments)
        self._process_args(arguments)
        sys.exit(0)

    ### PRIVATE METHODS ###

    def _handle_help_command(self, unknown_args):
        aliases = self.cli_aliases
        program_names = self.cli_program_names
        cli_class = None
        if (
            len(unknown_args) == 2
            and unknown_args[0] in aliases
            and unknown_args[1] in aliases[unknown_args[0]]
        ):
            cli_class = aliases[unknown_args[0]][unknown_args[1]]
        elif (
            len(unknown_args) == 1
            and unknown_args[0] in aliases
            and not isinstance(aliases[unknown_args[0]], dict)
        ):
            cli_class = aliases[unknown_args[0]]
        elif len(unknown_args) == 1 and unknown_args[0] in program_names:
            cli_class = program_names[unknown_args[0]]
        elif not len(unknown_args):
            self(["--help"])
            return
        if cli_class:
            instance = cli_class()
            print(instance.formatted_help)
        else:
            print("Cannot resolve {} to subcommand.".format(unknown_args))

    def _handle_list_command(self):
        by_scripting_group = {}
        for cli_class in self.cli_classes:
            instance = cli_class()
            scripting_group = getattr(instance, "scripting_group", None)
            group = by_scripting_group.setdefault(scripting_group, [])
            group.append(instance)
        print()
        if None in by_scripting_group:
            group = by_scripting_group.pop(None)
            for instance in sorted(group, key=lambda x: x.alias):
                message = "{}: {}".format(instance.alias, instance.short_description)
                print(message)
            print()
        for group, instances in sorted(by_scripting_group.items()):
            print("[{}]".format(group))
            for instance in sorted(instances, key=lambda x: x.alias):
                message = "    {}: {}".format(
                    instance.alias, instance.short_description
                )
                print(message)
            print()

    def _process_args(self, arguments):
        arguments, unknown_args = arguments
        if arguments.subparser_name == "help":
            self._handle_help_command(unknown_args)
        elif arguments.subparser_name == "list":
            self._handle_list_command()
        else:
            if hasattr(arguments, "subsubparser_name"):
                cli_class = self.cli_aliases[arguments.subparser_name][
                    arguments.subsubparser_name
                ]
            elif getattr(arguments, "subparser_name"):
                cli_class = self.cli_aliases[arguments.subparser_name]
            elif getattr(arguments, "subparser_name") is None:
                self(["--help"])
                return
            instance = cli_class()
            instance(unknown_args)

    def _setup_argument_parser(self, parser):
        subparsers = parser.add_subparsers(dest="subparser_name", title="subcommands")
        subparsers.add_parser("help", add_help=False, help="print subcommand help")
        subparsers.add_parser("list", add_help=False, help="list subcommands")
        alias_map = self.cli_aliases
        for key in sorted(alias_map):
            if not isinstance(alias_map[key], dict):
                cli_class = alias_map[key]
                instance = cli_class()
                subparsers.add_parser(
                    key, add_help=False, help=instance.short_description
                )
            else:
                subkeys = sorted(alias_map[key])
                group_subparser = subparsers.add_parser(
                    key, help="{{{}}} subcommand(s)".format(", ".join(subkeys))
                )
                group_subparsers = group_subparser.add_subparsers(
                    dest="subsubparser_name", title="{} subcommands".format(key),
                )
                for subkey in subkeys:
                    cli_class = alias_map[key][subkey]
                    instance = cli_class()
                    group_subparsers.add_parser(
                        subkey, add_help=False, help=instance.short_description
                    )

    ### PUBLIC PROPERTIES ###

    @property
    def cli_aliases(self):
        """
        Developer script aliases.
        """
        scripting_groups = []
        aliases = {}
        for cli_class in self.cli_classes:
            instance = cli_class()
            if getattr(instance, "alias", None):
                scripting_group = getattr(instance, "scripting_group", None)
                if scripting_group:
                    scripting_groups.append(scripting_group)
                    entry = (scripting_group, instance.alias)
                    if (scripting_group,) in aliases:
                        message = "alias conflict between scripting group"
                        message += " {!r} and {}"
                        message = message.format(
                            scripting_group, aliases[(scripting_group,)].__name__
                        )
                        raise Exception(message)
                    if entry in aliases:
                        message = "alias conflict between {} and {}"
                        message = message.format(
                            aliases[entry].__name__, cli_class.__name__
                        )
                        raise Exception(message)
                    aliases[entry] = cli_class
                else:
                    entry = (instance.alias,)
                    if entry in scripting_groups:
                        message = "alias conflict between {}"
                        message += " and scripting group {!r}"
                        message = message.format(cli_class.__name__, instance.alias)
                        raise Exception(message)
                    if entry in aliases:
                        message = "alias conflict be {} and {}"
                        message = message.format(cli_class.__name__, aliases[entry])
                        raise Exception(message)
                    aliases[(instance.alias,)] = cli_class
            else:
                if instance.program_name in scripting_groups:
                    message = "Alias conflict between {}"
                    message += " and scripting group {!r}"
                    message = message.format(cli_class.__name__, instance.program_name)
                    raise Exception(message)
                aliases[(instance.program_name,)] = cli_class
        alias_map = {}
        for key, value in aliases.items():
            if len(key) == 1:
                alias_map[key[0]] = value
            else:
                if key[0] not in alias_map:
                    alias_map[key[0]] = {}
                alias_map[key[0]][key[1]] = value
        return alias_map

    @abc.abstractproperty
    def cli_classes(self):
        """
        Developer scripts classes.
        """
        return []

    @property
    def cli_program_names(self):
        """
        Developer script program names.
        """
        program_names = {}
        for cli_class in self.cli_classes:
            instance = cli_class()
            program_names[instance.program_name] = cli_class
        return program_names
