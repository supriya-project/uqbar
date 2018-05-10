import collections
import inspect


def _dispatch_formatting(expr):
    if isinstance(expr, (list, tuple)):
        return get_sequence_repr(expr)
    return repr(expr)


def get_sequence_repr(expr):
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


def get_object_hash(expr):
    args, var_args, kwargs = get_object_vars(expr)
    hash_values = [type(expr)]
    hash_values.append(tuple(args.items()))
    hash_values.append(tuple(var_args))
    hash_values.append(tuple(sorted(kwargs.items())))
    return hash(tuple(hash_values))


def get_object_repr(expr, multiline=False):
    signature = get_object_signature(expr)
    defaults = {}
    for name, parameter in signature.parameters.items():
        if parameter.default is not inspect._empty:
            defaults[name] = parameter.default

    new_args, new_var_args, new_kwargs = get_object_vars(expr)
    args_parts = collections.OrderedDict()
    var_args_parts = []
    kwargs_parts = {}
    has_new_lines = multiline
    parts = []

    # Format keyword-optional arguments.
    for key, value in new_args.items():
        arg_repr = _dispatch_formatting(value)
        if '\n' in arg_repr:
            has_new_lines = True
        # If we don't have *args, we can use key=value formatting.
        # We can also omit arguments which match the signature's defaults.
        if not new_var_args:
            if key in defaults and value == defaults[key]:
                continue
            arg_repr = '{}={}'.format(key, arg_repr)
        args_parts[key] = arg_repr

    # Format *args
    for arg in new_var_args:
        arg_repr = _dispatch_formatting(arg)
        if '\n' in arg_repr:
            has_new_lines = True
        var_args_parts.append(arg_repr)

    # Format **kwargs
    for key, value in sorted(new_kwargs.items()):
        if key in defaults and value == defaults[key]:
            continue
        value = _dispatch_formatting(value)
        arg_repr = '{}={}'.format(key, value)
        has_new_lines = True
        kwargs_parts[key] = arg_repr

    # If we have *args, the initial args cannot use key/value formatting.
    if var_args_parts:
        for part in args_parts.values():
            parts.append(part)
        parts.extend(var_args_parts)
        for _, part in sorted(kwargs_parts.items()):
            parts.append(part)

    # Otherwise, we can combine and sort all key/value pairs.
    else:
        args_parts.update(kwargs_parts)
        for _, part in sorted(args_parts.items()):
            parts.append(part)

    # If we should format on multiple lines, add the appropriate formatting.
    if has_new_lines and parts:
        for i, part in enumerate(parts):
            parts[i] = '\n'.join('    ' + line for line in part.split('\n'))
        parts.append('    )')
        parts = ',\n'.join(parts)
        return '{}(\n{}'.format(type(expr).__name__, parts)

    parts = ', '.join(parts)
    return '{}({})'.format(type(expr).__name__, parts)


def get_object_signature(expr):
    if hasattr(expr, '__init__'):
        return inspect.signature(expr.__init__)
    elif hasattr(expr, '__new__'):
        return inspect.signature(expr.__new__)
    raise TypeError(type(expr))


def get_object_vars(expr):
    # print('VARS?', type(expr))
    signature = get_object_signature(expr)
    args = collections.OrderedDict()
    var_args = []
    kwargs = {}
    if expr is None:
        return args, var_args, kwargs
    for i, (name, parameter) in enumerate(signature.parameters.items()):
        # print('   ', parameter)
        if parameter.kind is inspect._POSITIONAL_ONLY:
            try:
                args[name] = getattr(expr, name)
            except AttributeError:
                args[name] = expr[name]
        elif parameter.kind is inspect._POSITIONAL_OR_KEYWORD:
            try:
                args[name] = getattr(expr, name)
            except AttributeError:
                args[name] = expr[name]
        elif parameter.kind is inspect._VAR_POSITIONAL:
            try:
                var_args.extend(expr[:])
            except TypeError:
                var_args.extend(getattr(expr, name))
        elif parameter.kind is inspect._KEYWORD_ONLY:
            try:
                kwargs[name] = getattr(expr, name)
            except AttributeError:
                kwargs[name] = expr[name]
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
    """
    # TODO: Clarify old vs. new variable naming here.
    new_args, new_var_args, new_kwargs = get_object_vars(expr)
    # print('OLD', new_args, new_var_args, new_kwargs)
    # print('NEW', type(expr), args, kwargs)
    if args:
        new_var_args = args
    for key, value in kwargs.items():
        if key in new_args:
            new_args[key] = value
        else:
            new_kwargs[key] = value
    new_args = list(new_args.values()) + list(new_var_args)
    return type(expr)(*new_args, **new_kwargs)
