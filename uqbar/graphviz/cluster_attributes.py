from uqbar.graphviz.attributes import Attributes


class ClusterAttributes:

    _styles = frozenset(['bold', 'dashed', 'dotted', 'filled', 'rounded',
        'solid', 'striped'])

    _valid_attributes = frozenset([
        'area',
        'bgcolor',
        'color',
        'colorscheme',
        'fillcolor',
        'fontcolor',
        'fontname',
        'fontsize',
        'gradientangle',
        'href',
        'id',
        'label',
        'labeljust',
        'labelloc',
        'layer',
        'lheight',
        'lp',
        'lwidth',
        'margin',
        'nojustify',
        'pencolor',
        'penwidth',
        'peripheries',
        'sortv',
        'style',
        'target',
        'tooltip',
        ])

    _validator_overrides = {}

    def __init__(self, **kwargs):
        Attributes.__init__(self, **kwargs)
