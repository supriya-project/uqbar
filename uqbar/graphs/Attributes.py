import abc
import collections
from uqbar.graphs.Color import Color
from uqbar.graphs.Point import Point


class Attributes(collections.Mapping):
    """
    Abstract base for Graphviz attributes classes.
    """

    ### CLASS VARIABLES ###

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
        'tripleoctagon', 'underline', 'utr'])

    _smooth_types = frozenset(['avg_dist', 'graph_dist', 'none', 'power_dist',
        'rng', 'spring', 'triangle'])

    _styles = frozenset()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, **kwargs):
        self._attributes = {}
        for key, value in kwargs.items():
            if key not in self._valid_attributes:
                raise ValueError(key)
            if key in self._validator_overrides:
                validators = self._validator_overrides[key]
            elif key in self._validators:
                validators = self._validators[key]
            else:
                raise ValueError
            if not isinstance(validators, tuple):
                validators = (validators,)
            for validator in validators:
                if isinstance(validator, str) and str(value) == validator:
                    value = str(value)
                    break
                elif isinstance(validator, type):
                    try:
                        value = validator(value)
                    except:
                        continue
                else:
                    try:
                        value = validator(self, value)
                    except:
                        continue
            self._attributes[key] = value

    ### SPECIAL METHODS ###

    def __getitem__(self, key):
        return self._attributes[key]

    def __iter__(self):
        return iter(self._attributes)

    def __len__(self):
        return len(self._attributes)

    ### VALIDATORS ###

    def _validate_arrow_type(self, value):
        value = str(value)
        assert value in self._arrow_types
        return value

    def _validate_cluster_mode(self, value):
        value = str(value)
        assert value in self._cluster_modes
        return value

    def _validate_color(self, value):
        if isinstance(value, Color):
            return value
        value = Color(value)
        return value

    def _validate_colors(self, value):
        if isinstance(value, (Color, str)):
            return self._validate_color(value)
        assert len(value)
        value = tuple(self._validate_color(_) for _ in value)
        if len(value) == 1:
            return value[0]
        return value

    def _validate_dir_type(self, value):
        value = str(value)
        assert value in self._dir_types
        return value

    def _validate_floats(self, value):
        assert len(value)
        return tuple(float(_) for _ in value)

    def _validate_output_mode(self, value):
        value = str(value)
        assert value in self._output_modes
        return value

    def _validate_pack_mode(self, value):
        value = str(value)
        assert value in self._pack_modes
        return value

    def _validate_page_dir(self, value):
        value = str(value)
        assert value in self._page_dirs
        return value

    def _validate_point(self, value):
        if isinstance(value, Point):
            return value
        value = Point(*value)
        return value

    def _validate_points(self, value_list):
        assert value_list
        return tuple(self._validate_point(_) for _ in value_list)

    def _validate_quad_type(self, value):
        value = str(value)
        assert value in self._quad_types
        return value

    def _validate_rank_dir(self, value):
        value = str(value)
        assert value in self._rank_dirs
        return value

    def _validate_rank_type(self, value):
        value = str(value)
        assert value in self._rank_types
        return value

    def _validate_rect(self, value):
        assert len(value) == 4
        value = tuple(float(_) for _ in value)
        return value

    def _validate_shape(self, value):
        value = str(value)
        assert value in self._shapes
        return value

    def _validate_smooth_type(self, value):
        value = str(value)
        assert value in self._smooth_types
        return value

    def _validate_style(self, value):
        value = str(value)
        assert value in self._styles
        return value

    def _validate_styles(self, value):
        if isinstance(value, str):
            return self._validate_style(value)
        assert value
        return tuple(self._validate_style(_) for _ in value)

    _validators = {
        'Damping': float,
        'K': float,
        'URL': str,
        '_background': str,
        'area': float,
        'arrowhead': _validate_arrow_type,
        'arrowsize': float,
        'arrowtail': _validate_arrow_type,
        'bb': _validate_rect,
        'bgcolor': _validate_colors,
        'center': bool,
        'charset': str,
        'clusterrank': _validate_cluster_mode,
        'color': _validate_colors,
        'colorscheme': str,
        'comment': str,
        'compound': bool,
        'concentrate': bool,
        'constraint': bool,
        'decorate': bool,
        'defaultdist': float,
        'dim': int,
        'dimen': int,
        'dir': _validate_dir_type,
        'diredgeconstraints': ('hier', bool),
        'distortion': float,
        'dpi': float,
        'edgeURL': str,
        'edgehref': str,
        'edgetarget': str,
        'edgetooltip': str,
        'epsilon': float,
        'esep': (float, _validate_point),
        'fillcolor': _validate_colors,
        'fixedsize': ('shape', bool),
        'fontcolor': _validate_color,
        'fontname': str,
        'fontnames': str,
        'fontpath': str,
        'fontsize': float,
        'forcelabels': bool,
        'gradientangle': int,
        'group': str,
        'headURL': str,
        'head_lp': _validate_point,
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
        'labelfontcolor': _validate_color,
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
        'lp': _validate_point,
        'ltail': str,
        'lwidth': float,
        'margin': (float, _validate_point),
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
        'outputorder': _validate_output_mode,
        'overlap': ('scale', 'scalexy', 'compress', 'ipsep', 'prism', bool),
        'overlap_scaling': float,
        'overlap_shrink': bool,
        'pack': bool,
        'packmode': _validate_pack_mode,
        'pad': (float, _validate_point),
        'page': (float, _validate_point),
        'pagedir': _validate_page_dir,
        'pencolor': _validate_color,
        'penwidth': float,
        'peripheries': int,
        'pin': bool,
        'pos': _validate_point,
        'quadtree': (_validate_quad_type, bool),
        'quantum': float,
        'rank': _validate_rank_type,
        'rankdir': _validate_rank_dir,
        'ranksep': (float, _validate_floats),
        'ratio': ('fill', 'compress', 'expand', 'auto', float),
        'rects': _validate_rect,
        'regular': bool,
        'remincross': bool,
        'repulsiveforce': float,
        'resolution': float,
        'root': str,
        'rotate': int,
        'rotation': float,
        'samehead': str,
        'sametail': str,
        'samplepoints': int,
        'scale': (float, _validate_point),
        'searchsize': int,
        'sep': (float, _validate_point),
        'shape': _validate_shape,
        'shapefile': str,
        'showboxes': int,
        'sides': int,
        'size': (float, _validate_point),
        'skew': float,
        'smoothing': _validate_smooth_type,
        'sortv': int,
        'splines': ('none', 'line', 'polyline', 'curved', 'ortho', 'spline', bool),
        'start': str,
        'style': _validate_styles,
        'stylesheet': str,
        'tailURL': str,
        'tail_lp': _validate_point,
        'tailclip': bool,
        'tailhref': str,
        'taillabel': str,
        'tailport': str,
        'tailtarget': str,
        'tailtooltip': str,
        'target': str,
        'tooltip': str,
        'truecolor': bool,
        'vertices': _validate_points,
        'viewport': str,
        'voro_margin': float,
        'weight': int,
        'width': float,
        'xdotversion': str,
        'xlabel': str,
        'xlp': _validate_point,
        'z': float,
        }
