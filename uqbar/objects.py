import collections
import inspect


def _dispatch_formatting(expr):
    if isinstance(expr, (list, tuple)):
        return _get_sequence_repr(expr)
    return repr(expr)


def _get_object_signature(expr):
    expr = type(expr)
    # print('E-I-ID', id(expr.__init__))
    # print('E-N-ID', id(expr.__new__))
    # print('o-I-ID', id(object.__init__))
    # print('o-N-ID', id(object.__new__))
    # print('IEQ?', expr.__init__ == object.__init__)
    # print('NEQ?', expr.__new__ == object.__new__)
    # attrs = {_.name: _ for _ in inspect.classify_class_attrs(expr)}
    # print('I?', attrs['__init__'])
    # print('N?', attrs['__new__'])
    if expr.__new__ is not object.__new__:
        return inspect.signature(expr.__new__)
    if expr.__init__ is not object.__init__:
        return inspect.signature(expr.__init__)
    return None


def _get_sequence_repr(expr):
    prototype = (bool, int, float, str, type(None))
    if all(isinstance(x, prototype) for x in expr):
        result = repr(expr)
        if len(result) < 50:
            return result
    if isinstance(expr, list):
        braces = '[', ']'
    else:
        braces = '(', ')'
    result = [braces[0]]
    for x in expr:
        for line in repr(x).splitlines():
            result.append('    ' + line)
        result[-1] += ','
    result.append('    ' + braces[-1])
    return '\n'.join(result)


def compare_objects(object_one, object_two, coerce=False):
    if coerce:
        try:
            object_two = type(object_one)(object_two)
        except (ValueError, TypeError):
            return False
    object_one_values = type(object_one), get_vars(object_one)
    try:
        object_two_values = type(object_two), get_vars(object_two)
    except AttributeError:
        object_two_values = type(object_two), object_two
    return object_one_values == object_two_values


def get_hash(expr):
    args, var_args, kwargs = get_vars(expr)
    hash_values = [type(expr)]
    for key, value in args.items():
        if isinstance(value, list):
            value = tuple(value)
        elif isinstance(value, set):
            value = frozenset(value)
        elif isinstance(value, dict):
            value = tuple(sorted(value.items()))
        args[key] = value
    hash_values.append(tuple(args.items()))
    hash_values.append(tuple(var_args))
    for key, value in kwargs.items():
        if isinstance(value, list):
            value = tuple(value)
        elif isinstance(value, set):
            value = frozenset(value)
        elif isinstance(value, dict):
            value = tuple(sorted(value.items()))
        kwargs[key] = value
    hash_values.append(tuple(sorted(kwargs.items())))
    return hash(tuple(hash_values))


def get_repr(expr, multiline=False):
    """
    Build a repr string for ``expr`` from its vars and signature.

    ::

        >>> class MyObject:
        ...     def __init__(self, arg1, arg2, *var_args, foo=None, bar=None, **kwargs):
        ...         self.arg1 = arg1
        ...         self.arg2 = arg2
        ...         self.var_args = var_args
        ...         self.foo = foo
        ...         self.bar = bar
        ...         self.kwargs = kwargs
        ...
        >>> my_object = MyObject('a', 'b', 'c', 'd', foo='x', quux=['y', 'z'])

    ::

        >>> import uqbar
        >>> print(uqbar.objects.get_repr(my_object))
        MyObject(
            'a',
            'b',
            'c',
            'd',
            foo='x',
            quux=['y', 'z'],
            )

    """
    signature = _get_object_signature(expr)
    if signature is None:
        return '{}()'.format(type(expr).__name__)

    defaults = {}
    for name, parameter in signature.parameters.items():
        if parameter.default is not inspect._empty:
            defaults[name] = parameter.default

    args, var_args, kwargs = get_vars(expr)
    args_parts = collections.OrderedDict()
    var_args_parts = []
    kwargs_parts = {}
    has_lines = multiline
    parts = []

    # Format keyword-optional arguments.
    # print(type(expr), args)
    for i, (key, value) in enumerate(args.items()):
        arg_repr = _dispatch_formatting(value)
        if '\n' in arg_repr:
            has_lines = True
        args_parts[key] = arg_repr

    # Format *args
    for arg in var_args:
        arg_repr = _dispatch_formatting(arg)
        if '\n' in arg_repr:
            has_lines = True
        var_args_parts.append(arg_repr)

    # Format **kwargs
    for key, value in sorted(kwargs.items()):
        if key in defaults and value == defaults[key]:
            continue
        value = _dispatch_formatting(value)
        arg_repr = '{}={}'.format(key, value)
        has_lines = True
        kwargs_parts[key] = arg_repr

    for _, part in args_parts.items():
        parts.append(part)
    parts.extend(var_args_parts)
    for _, part in sorted(kwargs_parts.items()):
        parts.append(part)

    # If we should format on multiple lines, add the appropriate formatting.
    if has_lines and parts:
        for i, part in enumerate(parts):
            parts[i] = '\n'.join('    ' + line for line in part.split('\n'))
        parts.append('    )')
        parts = ',\n'.join(parts)
        return '{}(\n{}'.format(type(expr).__name__, parts)

    parts = ', '.join(parts)
    return '{}({})'.format(type(expr).__name__, parts)


def get_vars(expr):
    """
    Get ``args``, ``var args`` and ``kwargs`` for an object ``expr``.

    ::

        >>> class MyObject:
        ...     def __init__(self, arg1, arg2, *var_args, foo=None, bar=None, **kwargs):
        ...         self.arg1 = arg1
        ...         self.arg2 = arg2
        ...         self.var_args = var_args
        ...         self.foo = foo
        ...         self.bar = bar
        ...         self.kwargs = kwargs
        ...
        >>> my_object = MyObject('a', 'b', 'c', 'd', foo='x', quux=['y', 'z'])

    ::

        >>> import uqbar
        >>> args, var_args, kwargs = uqbar.objects.get_vars(my_object)

    ::

        >>> args
        OrderedDict([('arg1', 'a'), ('arg2', 'b')])

    ::

        >>> var_args
        ['c', 'd']

    ::

        >>> kwargs
        {'foo': 'x', 'quux': ['y', 'z']}

    """
    # print('TYPE?', type(expr))
    signature = _get_object_signature(expr)
    if signature is None:
        return ({}, [], {})
    # print('SIG?', signature)
    args = collections.OrderedDict()
    var_args = []
    kwargs = {}
    if expr is None:
        return args, var_args, kwargs
    for i, (name, parameter) in enumerate(signature.parameters.items()):
        # print('   ', parameter)

        if i == 0 and name in ('self', 'cls', 'class_', 'klass'):
            continue

        if parameter.kind is inspect._POSITIONAL_ONLY:
            try:
                args[name] = getattr(expr, name)
            except AttributeError:
                args[name] = expr[name]

        elif (
            parameter.kind is inspect._POSITIONAL_OR_KEYWORD or
            parameter.kind is inspect._KEYWORD_ONLY
        ):
            found = False
            for x in (name, '_' + name):
                try:
                    value = getattr(expr, x)
                    found = True
                    break
                except AttributeError:
                    try:
                        value = expr[x]
                        found = True
                        break
                    except (KeyError, TypeError):
                        pass
            if not found:
                raise ValueError('Cannot find value for {!r}'.format(name))
            if parameter.default is inspect._empty:
                args[name] = value
            elif parameter.default != value:
                kwargs[name] = value

        elif parameter.kind is inspect._VAR_POSITIONAL:
            value = None
            try:
                value = expr[:]
            except TypeError:
                value = getattr(expr, name)
            if value:
                var_args.extend(value)

        elif parameter.kind is inspect._VAR_KEYWORD:
            items = {}
            if hasattr(expr, 'items'):
                items = expr.items()
            elif hasattr(expr, name):
                mapping = getattr(expr, name)
                if not isinstance(mapping, dict):
                    mapping = dict(mapping)
                items = mapping.items()
            elif hasattr(expr, '_' + name):
                mapping = getattr(expr, '_' + name)
                if not isinstance(mapping, dict):
                    mapping = dict(mapping)
                items = mapping.items()
            for key, value in items:
                if key not in args:
                    kwargs[key] = value

    return args, var_args, kwargs


def new(expr, *args, **kwargs):
    """
    Template an object.

    ::

        >>> class MyObject:
        ...     def __init__(self, arg1, arg2, *var_args, foo=None, bar=None, **kwargs):
        ...         self.arg1 = arg1
        ...         self.arg2 = arg2
        ...         self.var_args = var_args
        ...         self.foo = foo
        ...         self.bar = bar
        ...         self.kwargs = kwargs
        ...
        >>> my_object = MyObject('a', 'b', 'c', 'd', foo='x', quux=['y', 'z'])

    ::

        >>> import uqbar
        >>> new_object = uqbar.objects.new(my_object, foo=666, bar=1234)
        >>> print(uqbar.objects.get_repr(new_object))
        MyObject(
            'a',
            'b',
            'c',
            'd',
            bar=1234,
            foo=666,
            quux=['y', 'z'],
            )

    Original object is unchanged:

    ::

        >>> print(uqbar.objects.get_repr(my_object))
        MyObject(
            'a',
            'b',
            'c',
            'd',
            foo='x',
            quux=['y', 'z'],
            )

    """
    # TODO: Clarify old vs. new variable naming here.
    current_args, current_var_args, current_kwargs = get_vars(expr)
    new_kwargs = current_kwargs.copy()

    recursive_arguments = {}
    for key in tuple(kwargs):
        if '__' in key:
            value = kwargs.pop(key)
            key, _, subkey = key.partition('__')
            recursive_arguments.setdefault(key, []).append((subkey, value))

    for key, pairs in recursive_arguments.items():
        recursed_object = current_args.get(key, current_kwargs.get(key))
        if recursed_object is None:
            continue
        kwargs[key] = new(recursed_object, **dict(pairs))

    if args:
        current_var_args = args
    for key, value in kwargs.items():
        if key in current_args:
            current_args[key] = value
        else:
            new_kwargs[key] = value

    new_args = list(current_args.values()) + list(current_var_args)
    return type(expr)(*new_args, **new_kwargs)
