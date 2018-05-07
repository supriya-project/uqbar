import collections
import enum
import math
import re
import uqbar.graphs  # noqa
from typing import Any, FrozenSet, Mapping, Optional, Union


class Attributes(collections.MutableMapping):
    """
    An attributes listing for a Graphviz graph, cluster, node or edge.

    ::

        >>> import uqbar.graphs
        >>> attributes = uqbar.graphs.Attributes(
        ...     'node',
        ...     color='black',
        ...     fillcolor='white',
        ...     shape='Mrecord',
        ...     style=['rounded', 'filled'],
        ...     )

    ::

        >>> print(format(attributes, 'graphviz'))
        [color=black,
            fillcolor=white,
            shape=Mrecord,
            style="rounded, filled"];

    """

    ### CLASS VARIABLES ###

    class Color(object):

        __slots__ = ('color',)

        def __init__(self, color) -> None:
            self.color = str(color)

        def __eq__(self, other) -> bool:
            return (
                type(self) == type(other) and
                self.color == other.color
                )

        def __repr__(self) -> str:
            return '<Color {!r}>'.format(self.color)

    class Mode(enum.Enum):
        CLUSTER = 1
        EDGE = 2
        GRAPH = 3
        NODE = 4
        TABLE = 5
        TABLE_CELL = 6

    class Point(object):

        __slots__ = ('x', 'y')

        def __init__(self, x, y) -> None:
            self.x = float(x)
            self.y = float(y)

        def __eq__(self, other) -> bool:
            return (
                type(self) == type(other) and
                self.x == other.x and
                self.y == other.y
                )

    __documentation_section__ = 'Core Classes'

    _arrow_types = frozenset(['box', 'circle', 'crow', 'diamond', 'dot',
        'ediamond', 'empty', 'halfopen', 'inv', 'invdot', 'invempty',
        'invodot', 'none', 'normal', 'obox', 'odiamond', 'odot', 'open', 'tee',
        'vee'])

    _cluster_modes = frozenset(['global', 'local', 'none'])

    _dir_types = frozenset(['back', 'both', 'forward', 'none'])

    _output_modes = frozenset(['breadthfirst', 'nodesfirst', 'edgesfirst'])

    _pack_modes = frozenset(['node', 'clust', 'graph'])

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
        'tripleoctagon', 'underline', 'utr', 'record', 'Mrecord'])

    _smooth_types = frozenset(['avg_dist', 'graph_dist', 'none', 'power_dist',
        'rng', 'spring', 'triangle'])

    _styles: FrozenSet[str] = frozenset()

    _word_pattern = re.compile('^\w+$')

    ### GRAPH OBJECT SPECIFICS ###

    _cluster_attributes = frozenset(['K', 'URL', 'area', 'bgcolor', 'color',
        'colorscheme', 'fillcolor', 'fontcolor', 'fontname', 'fontsize',
        'gradientangle', 'href', 'id', 'label', 'labeljust', 'labelloc',
        'layer', 'lheight', 'lp', 'lwidth', 'margin', 'nojustify', 'pencolor',
        'penwidth', 'peripheries', 'sortv', 'style', 'target', 'tooltip'])

    _cluster_styles = frozenset(['bold', 'dashed', 'dotted', 'filled',
        'rounded', 'solid', 'striped'])

    _edge_attributes = frozenset(['arrowhead', 'arrowsize', 'arrowtail',
        'color', 'colorscheme', 'comment', 'constraint', 'decorate', 'dir',
        'edgeURL', 'edgehref', 'edgetarget', 'edgetooltip', 'fillcolor',
        'fontcolor', 'fontname', 'fontsize', 'headURL', 'head_lp', 'headclip',
        'headhref', 'headlabel', 'headport', 'headtarget', 'headtooltip',
        'href', 'id', 'label', 'labelURL', 'labelangle', 'labeldistance',
        'labelfloat', 'labelfontcolor', 'labelfontname', 'labelfontsize',
        'labelhref', 'labeltarget', 'labeltooltip', 'layer', 'len', 'lhead',
        'lp', 'ltail', 'minlen', 'nojustify', 'penwidth', 'pos', 'samehead',
        'sametail', 'showboxes', 'style', 'tailURL', 'tail_lp', 'tailclip',
        'tailhref', 'taillabel', 'tailport', 'tailtarget', 'tailtooltip',
        'target', 'tooltip', 'weight'])

    _edge_styles = frozenset(['bold', 'dashed', 'dotted', 'solid'])

    _graph_attributes = frozenset(['Damping', 'K', 'URL', 'bb', 'bgcolor',
        'center', 'charset', 'clusterrank', 'color', 'colorscheme', 'comment',
        'compound', 'concentrate', 'defaultdist', 'dim', 'dimen',
        'diredgeconstraints', 'dpi', 'epsilon', 'esep', 'fontcolor',
        'fontname', 'fontnames', 'fontpath', 'fontsize', 'forcedlabels',
        'gradientangle', 'href', 'id', 'imagepath', 'inputscale', 'label',
        'label_scheme', 'labeljust', 'labelloc', 'landscape', 'layerlistsep',
        'layers', 'layerselect', 'layersep', 'layout', 'levels', 'levelsgap',
        'lheight', 'lp', 'lwidth', 'margin', 'maxiter', 'mclimit', 'mode',
        'model', 'mosek', 'newrank', 'nodesep', 'nojustify', 'normalize',
        'notranslate', 'nslimit', 'nslimit1', 'ordering', 'orientation',
        'outputorder', 'overlap', 'overlap_scaling', 'overlap_shrink', 'pack',
        'packmode', 'pad', 'page', 'pagedir', 'quadtree', 'quantum', 'rank',
        'rankdir', 'ranksep', 'remincross', 'repulsiveforce', 'resolution',
        'root', 'rotate', 'rotation', 'scale', 'searchsize', 'sep',
        'showboxes', 'size', 'smoothing', 'sortv', 'splines', 'start', 'style',
        'stylesheet', 'target', 'truecolor', 'viewport', 'voro_margin',
        'xdotversion', 'xlabel', 'xlp', 'penwidth'])

    _graph_styles = _cluster_styles

    _node_attributes = frozenset(['URL', 'area', 'color', 'colorscheme',
        'comment', 'distortion', 'fillcolor', 'fixedsize', 'fontcolor',
        'fontname', 'fontsize', 'gradientangle', 'group', 'height', 'href',
        'id', 'image', 'imagepos', 'imagescale', 'label', 'labelloc', 'layer',
        'margin', 'nojustify', 'ordering', 'orientation', 'penwidth',
        'peripheries', 'pin', 'pos', 'rects', 'regular', 'root',
        'samplepoints', 'shape', 'shapefile', 'showboxes', 'sides', 'skew',
        'sortv', 'style', 'target', 'tooltip', 'vertixes', 'width', 'z'])

    _node_styles = frozenset(['solid', 'dashed', 'dotted', 'bold', 'rounded',
        'diagonals', 'filled', 'striped', 'wedged'])

    ### HTML OBJECT SPECIFICS ###

    _table_attributes = frozenset(['align', 'bgcolor', 'border', 'cellborder',
        'cellpadding', 'cellspacing', 'color', 'columns', 'fixedsize',
        'gradientangle', 'height', 'href', 'id', 'rows', 'sides', 'style',
        'target', 'title', 'tooltip', 'valign', 'width'])

    _table_cell_attributes = frozenset(['align', 'balign', 'bgcolor', 'border',
        'cellpadding', 'cellspacing', 'color', 'colspan', 'fixedsize',
        'gradientangle', 'height', 'href', 'id', 'rowspan', 'sides', 'style',
        'target', 'title', 'tooltip', 'valign', 'width'])

    ### VALIDATORS ###

    _validators: Optional[Mapping[str, object]] = None

    ### INITIALIZER ###

    def __init__(
        self,
        mode: Union[str, 'uqbar.graphs.Attributes.Mode'],
        **kwargs,
        ) -> None:
        if not isinstance(mode, self.Mode):
            mode = self.Mode[str(mode).upper()]
        self._mode = mode
        self._attributes = self._validate_attributes(mode, **kwargs)

    ### SPECIAL METHODS ###

    def __delitem__(self, key: str) -> None:
        del(self._attributes[key])

    def __eq__(self, other) -> bool:
        return (
            type(self) == type(other) and
            self._mode == other._mode and
            self._attributes == other._attributes
            )

    def __format__(self, format_spec: str=None) -> str:
        if format_spec == 'graphviz':
            return self.__format_graphviz__()
        elif format_spec == 'html':
            return self.__format_html__()
        return str(self)

    def __format_graphviz__(self) -> str:
        if not self._attributes:
            return ''
        result = []
        attributes = sorted(self._attributes.items())
        for i, (key, value) in enumerate(attributes, 1):
            value = self._format_value(value).split('\n')
            value[0] = '{}={}'.format(key, value[0])
            if i < len(attributes):
                value[-1] += ','
            if i == 1:
                result.append(value.pop(0))
            result.extend('    ' + _ for _ in value)
        result[0] = '[' + result[0]
        result[-1] = result[-1] + '];'
        return '\n'.join(result)

    def __format_html__(self) -> str:
        if not self._attributes:
            return ''
        result = []
        for key, value in sorted(self._attributes.items()):
            value = self._format_value(value)
            if not value.startswith('"'):
                value = '"{}"'.format(value)
            result.append('{}={}'.format(key.upper(), value))
        return ' '.join(result)

    def __getitem__(self, key) -> Any:
        return self._attributes[key]

    def __iter__(self):
        return iter(self._attributes)

    def __len__(self):
        return len(self._attributes)

    def __setitem__(self, key, value):
        new_attributes = self._validate_attributes(
            self.mode, **{key: value})
        self._attributes.update(new_attributes)

    ### PRIVATE METHODS ###

    @classmethod
    def _format_value(cls, value) -> str:
        if isinstance(value, bool):
            return str(value).lower()
        elif isinstance(value, int):
            return str(value)
        elif isinstance(value, float):
            if not value % 1.0:
                value = math.floor(value)
            return str(value)
        elif isinstance(value, (list, tuple)):
            value = ', '.join(cls._format_value(x) for x in value)
            return cls._format_value(value)
        elif isinstance(value, cls.Color):
            return str(value.color)
        elif isinstance(value, str):
            if value.startswith('<') and value.endswith('>'):
                return value
            should_quote = False
            if not cls._word_pattern.match(value):
                should_quote = True
            elif value and value[0].isdigit():
                should_quote = True
            elif value.lower() in (
                'digraph',
                'edge',
                'graph',
                'node',
                'subgraph',
                ):
                should_quote = True
            if should_quote:
                value = value.replace('"', r'\"')
                value = '"{}"'.format(value)
            return value
        raise ValueError(value)

    @classmethod
    def _validate_arrow_type(cls, value, **kwargs):
        value = str(value)
        assert value in cls._arrow_types
        return value

    @classmethod
    def _validate_attributes(cls, mode, **kwargs):
        valid_attributes, valid_styles = {
            cls.Mode.CLUSTER: (cls._cluster_attributes, cls._cluster_styles),
            cls.Mode.EDGE: (cls._edge_attributes, cls._edge_styles),
            cls.Mode.GRAPH: (cls._graph_attributes, cls._graph_styles),
            cls.Mode.NODE: (cls._node_attributes, cls._node_styles),
            cls.Mode.TABLE: (cls._table_attributes, ()),
            cls.Mode.TABLE_CELL: (cls._table_cell_attributes, ()),
            }[mode]
        attributes = {}
        for key, value in kwargs.items():
            if key not in valid_attributes:
                raise ValueError(key)
            validators = cls._get_validators(mode)[key]
            if not isinstance(validators, tuple):
                validators = (validators,)
            for validator in validators:
                if isinstance(validator, str):
                    if str(value) == validator:
                        value = str(value)
                        break
                    continue
                elif isinstance(validator, type):
                    value = validator(value)
                    break
                else:
                    value = validator(value, valid_styles=valid_styles)
                    break
            attributes[key] = value
        return attributes

    @classmethod
    def _validate_cluster_mode(cls, value, **kwargs):
        value = str(value)
        assert value in cls._cluster_modes
        return value

    @classmethod
    def _validate_color(cls, value, **kwargs):
        if isinstance(value, cls.Color):
            return value
        value = cls.Color(value)
        return value

    @classmethod
    def _validate_colors(cls, value, **kwargs):
        if isinstance(value, (cls.Color, int, str)):
            return cls._validate_color(value, **kwargs)
        assert len(value)
        value = tuple(cls._validate_color(_, **kwargs) for _ in value)
        if len(value) == 1:
            return value[0]
        return value

    @classmethod
    def _validate_dir_type(cls, value, **kwargs):
        value = str(value)
        assert value in cls._dir_types
        return value

    @classmethod
    def _validate_floats(cls, value, **kwargs):
        assert len(value)
        return tuple(float(_) for _ in value)

    @classmethod
    def _validate_output_mode(cls, value, **kwargs):
        value = str(value)
        assert value in cls._output_modes
        return value

    @classmethod
    def _validate_pack_mode(cls, value, **kwargs):
        value = str(value)
        assert value in cls._pack_modes
        return value

    @classmethod
    def _validate_page_dir(cls, value, **kwargs):
        value = str(value)
        assert value in cls._page_dirs
        return value

    @classmethod
    def _validate_point(cls, value, **kwargs):
        if isinstance(value, cls.Point):
            return value
        value = cls.Point(*value)
        return value

    @classmethod
    def _validate_points(cls, value_list, **kwargs):
        assert value_list
        return tuple(cls._validate_point(_, **kwargs) for _ in value_list)

    @classmethod
    def _validate_quad_type(cls, value, **kwargs):
        value = str(value)
        assert value in cls._quad_types
        return value

    @classmethod
    def _validate_rank_dir(cls, value, **kwargs):
        value = str(value)
        assert value in cls._rank_dirs
        return value

    @classmethod
    def _validate_rank_type(cls, value, **kwargs):
        value = str(value)
        assert value in cls._rank_types
        return value

    @classmethod
    def _validate_rect(cls, value, **kwargs):
        assert len(value) == 4
        value = tuple(float(_) for _ in value)
        return value

    @classmethod
    def _validate_shape(cls, value, **kwargs):
        value = str(value)
        assert value in cls._shapes
        return value

    @classmethod
    def _validate_smooth_type(cls, value, **kwargs):
        value = str(value)
        assert value in cls._smooth_types
        return value

    @classmethod
    def _validate_style(cls, value, valid_styles=None, **kwargs):
        value = str(value)
        assert value in valid_styles
        return value

    @classmethod
    def _validate_styles(cls, value, valid_styles=None, **kwargs):
        if isinstance(value, str):
            return cls._validate_style(
                value,
                valid_styles=valid_styles,
                **kwargs
                )
        assert value
        return tuple(cls._validate_style(
            _, valid_styles=valid_styles, **kwargs
            ) for _ in value)

    ### PUBLIC METHODS ###

    def copy(self):
        return type(self)(self.mode, **self._attributes.copy())

    ### PUBLIC PROPERTIES ###

    @property
    def mode(self):
        return self._mode

    @classmethod
    def _get_validators(cls, mode):
        if not cls._validators:
            cls._validators = {
                'Damping': float,
                'K': float,
                'URL': str,
                '_background': str,
                'align': ('center', 'left', 'right', 'text'),
                'area': float,
                'arrowhead': Attributes._validate_arrow_type,
                'arrowsize': float,
                'arrowtail': Attributes._validate_arrow_type,
                'balign': ('center', 'left', 'right', 'text'),
                'bb': Attributes._validate_rect,
                'bgcolor': Attributes._validate_colors,
                'border': float,
                'cellborder': float,
                'cellpadding': float,
                'cellspacing': float,
                'center': bool,
                'charset': str,
                'clusterrank': Attributes._validate_cluster_mode,
                'color': Attributes._validate_colors,
                'colorscheme': str,
                'colspan': int,
                'columns': int,
                'comment': str,
                'compound': bool,
                'concentrate': bool,
                'constraint': bool,
                'decorate': bool,
                'defaultdist': float,
                'dim': int,
                'dimen': int,
                'dir': Attributes._validate_dir_type,
                'diredgeconstraints': ('hier', bool),
                'distortion': float,
                'dpi': float,
                'edgeURL': str,
                'edgehref': str,
                'edgetarget': str,
                'edgetooltip': str,
                'epsilon': float,
                'esep': (float, Attributes._validate_point),
                'fillcolor': Attributes._validate_colors,
                'fixedsize': ('shape', bool),
                'fontcolor': Attributes._validate_color,
                'fontname': str,
                'fontnames': str,
                'fontpath': str,
                'fontsize': float,
                'forcelabels': bool,
                'gradientangle': int,
                'group': str,
                'headURL': str,
                'head_lp': Attributes._validate_point,
                'headclip': bool,
                'headhref': str,
                'headlabel': str,
                'headport': str,
                'headtarget': str,
                'headtooltip': str,
                'height': float,
                'href': str,
                'id': str,
                'image': str,
                'imagepath': str,
                'imagepos': str,
                'imagescale': ('width', 'height', 'both', bool),
                'inputscale': float,
                'label': str,
                'labelURL': str,
                'label_scheme': int,
                'labelangle': float,
                'labeldistance': float,
                'labelfloat': bool,
                'labelfontcolor': Attributes._validate_color,
                'labelfontname': str,
                'labelfontsize': float,
                'labelhref': str,
                'labeljust': str,
                'labelloc': str,
                'labeltarget': str,
                'labeltooltip': str,
                'landscape': bool,
                'layer': str,
                'layerlistsep': str,
                'layers': str,
                'layerselect': str,
                'layersep': str,
                'layout': str,
                'len': float,
                'levels': int,
                'levelsgap': float,
                'lhead': str,
                'lheight': float,
                'lp': Attributes._validate_point,
                'ltail': str,
                'lwidth': float,
                'margin': (float, Attributes._validate_point),
                'maxiter': int,
                'mclimit': float,
                'mindist': float,
                'minlen': int,
                'mode': str,
                'model': str,
                'mosek': bool,
                'newrank': bool,
                'nodesep': float,
                'nojustify': bool,
                'normalize': (float, bool),
                'notranslate': bool,
                'nslimit': float,
                'nslimit1': float,
                'ordering': str,
                'outputorder': Attributes._validate_output_mode,
                'overlap': ('scale', 'scalexy', 'compress', 'ipsep', 'prism', bool),
                'overlap_scaling': float,
                'overlap_shrink': bool,
                'pack': bool,
                'packmode': Attributes._validate_pack_mode,
                'pad': (float, Attributes._validate_point),
                'page': (float, Attributes._validate_point),
                'pagedir': Attributes._validate_page_dir,
                'pencolor': Attributes._validate_color,
                'penwidth': float,
                'peripheries': int,
                'pin': bool,
                'pos': Attributes._validate_point,
                'quadtree': (Attributes._validate_quad_type, bool),
                'quantum': float,
                'rank': Attributes._validate_rank_type,
                'rankdir': Attributes._validate_rank_dir,
                'ranksep': (float, Attributes._validate_floats),
                'ratio': ('fill', 'compress', 'expand', 'auto', float),
                'rects': Attributes._validate_rect,
                'regular': bool,
                'remincross': bool,
                'repulsiveforce': float,
                'resolution': float,
                'root': str,
                'rotate': int,
                'rotation': float,
                'rows': int,
                'rowspan': int,
                'samehead': str,
                'sametail': str,
                'samplepoints': int,
                'scale': (float, Attributes._validate_point),
                'searchsize': int,
                'sep': (float, Attributes._validate_point),
                'shape': Attributes._validate_shape,
                'shapefile': str,
                'showboxes': int,
                'sides': (int, str),
                'size': (float, Attributes._validate_point),
                'skew': float,
                'smoothing': Attributes._validate_smooth_type,
                'sortv': int,
                'splines': ('none', 'line', 'polyline', 'curved', 'ortho', 'spline', bool),
                'start': str,
                'style': Attributes._validate_styles,
                'stylesheet': str,
                'tailURL': str,
                'tail_lp': Attributes._validate_point,
                'tailclip': bool,
                'tailhref': str,
                'taillabel': str,
                'tailport': str,
                'tailtarget': str,
                'tailtooltip': str,
                'target': str,
                'title': str,
                'tooltip': str,
                'truecolor': bool,
                'valign': ('middle', 'bottom', 'top'),
                'vertices': Attributes._validate_points,
                'viewport': str,
                'voro_margin': float,
                'weight': int,
                'width': float,
                'xdotversion': str,
                'xlabel': str,
                'xlp': Attributes._validate_point,
                'z': float,
                }
        return cls._validators
