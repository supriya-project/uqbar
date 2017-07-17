import abc


class Attributes:

    _arrow_types = frozenset(['box', 'circle', 'crow', 'diamond', 'dot',
        'ediamond', 'empty', 'halfopen', 'inv', 'invdot', 'invempty',
        'invodot', 'none', 'normal', 'obox', 'odiamond', 'odot', 'open', 'tee',
        'vee'])

    _cluster_modes = frozenset(['global', 'local', 'none'])

    _dir_types = frozenset(['back', 'both', 'forward', 'none'])

    _page_dirs = frozenset(['BL', 'BR', 'LB', 'LT', 'RB', 'RT', 'TL', 'TR'])

    _quad_types = frozenset(['fast', 'none', 'normal'])

    _rank_types = frozenset(['max', 'min', 'same', 'sink', 'source'])

    _rank_dirs = frozenset(['BT', 'LR', 'RL', 'TB'])

    _shapes = frozenset(['Mcircle', 'Mdiamond', 'Msquare', 'assembly', 'box',
        'box3d', 'cds', 'circle', 'component', 'cylinder', 'diamond',
        'doublecircle', 'doubleoctagon', 'egg', 'ellipse', 'fivepoverhang',
        'folder', 'hexagon', 'house', 'insulator', 'invhouse', 'invtrapezium',
        'invtriangle', 'larrow', 'lpromoter', 'none', 'note', 'noverhang',
        'octagon', 'oval', 'parallelogram', 'pentagon', 'plain', 'plaintext',
        'point', 'polygon', 'primersite', 'promoter', 'proteasesite',
        'proteinstab', 'rarrow', 'rect', 'rectangle', 'restrictionsite',
        'ribosite', 'rnastab', 'rpromoter', 'septagon', 'signature', 'square',
        'star', 'tab', 'terminator', 'threepoverhang', 'trapezium', 'triangle',
        'tripleoctagon', 'underline', 'utr'])

    _smooth_types = frozenset(['avg_dist', 'graph_dist', 'none', 'power_dist',
        'rng', 'spring', 'triangle'])

    _validators = {
        }

    @abc.abstractmethod
    def __init__(self, **kwargs):
        self._attributes = {}
        for key, value in kwargs.items():
            if key not in self._valid_attributes:
                raise ValueError(key)
            if key in self._validator_overrides:
                value = self._validator_overrides[key](value)
            elif key in self._validators:
                value = self._validators[key](value)
            self._attributes[key] = value
