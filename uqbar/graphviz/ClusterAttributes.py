from uqbar.graphviz.Attributes import Attributes


class ClusterAttributes(Attributes):
    """
    Graphviz cluster object attributes manifest.

    ::

        >>> import uqbar.graphviz
        >>> attributes = uqbar.graphviz.ClusterAttributes(
        ...     color='red',
        ...     style='dashed',
        ...     )

    ::

        >>> for item in sorted(attributes.items()):
        ...     item
        ...
        ('color', 'red')
        ('style', 'dashed')

    """

    _styles = frozenset(['bold', 'dashed', 'dotted', 'filled', 'rounded',
        'solid', 'striped'])

    _valid_attributes = frozenset([
        'K',
        'URL',
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
