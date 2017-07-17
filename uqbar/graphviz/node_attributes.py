from uqbar.graphviz.attributes import Attributes


class NodeAttributes:

    _styles = frozenset(['solid', 'dashed', 'dotted', 'bold', 'rounded',
        'diagonals', 'filled', 'striped', 'wedged'])

    _valid_attributes = frozenset([
        'area',
        'color',
        'colorscheme',
        'comment',
        'distortion',
        'fillcolor',
        'fixedsize',
        'fontcolor',
        'fontname',
        'fontsize',
        'gradientangle',
        'group',
        'height',
        'href',
        'id',
        'image',
        'imagepos',
        'imagescale',
        'label',
        'labelloc',
        'layer',
        'margin',
        'nojustify',
        'ordering',
        'orientation',
        'penwidth',
        'peripheries',
        'pin',
        'pos',
        'rects',
        'regular',
        'root',
        'samplepoints',
        'shape',
        'shapefile',
        'showboxes',
        'sides',
        'skew',
        'sortv',
        'style',
        'target',
        'tooltip',
        'vertixes',
        'width',
        'z',
        ])

    _validator_overrides = {}

    def __init__(self, **kwargs):
        Attributes.__init__(self, **kwargs)
