from uqbar.graphviz.Attributes import Attributes


class EdgeAttributes(Attributes):
    """
    Graphviz edge object attributes manifest.

    ::

        >>> import uqbar.graphviz
        >>> attributes = uqbar.graphiz.EdgeAttributes(
        ...     color='green',
        ...     style='dotted',
        ...     )

    ::

        >>> for item in sorted(attributes.items()):
        ...     item
        ...

    """

    _styles = frozenset(['bold', 'dashed', 'dotted', 'solid'])

    _valid_attributes = frozenset([
        'arrowhead',
        'arrowsize',
        'arrowtail',
        'color',
        'colorscheme',
        'comment',
        'constraint',
        'decorate',
        'dir',
        'edgeURL',
        'edgehref',
        'edgetarget',
        'edgetooltip',
        'fillcolor',
        'fontcolor',
        'fontname',
        'fontsize',
        'headURL',
        'head_lp',
        'headclip',
        'headhref',
        'headlabel',
        'headport',
        'headtarget',
        'headtooltip',
        'href',
        'id',
        'label',
        'labelURL',
        'labelangle',
        'labeldistance',
        'labelfloat',
        'labelfontcolor',
        'labelfontname',
        'labelfontsize',
        'labelhref',
        'labeltarget',
        'labeltooltip',
        'layer',
        'len',
        'lhead',
        'lp',
        'ltail',
        'minlen',
        'nojustify',
        'penwidth',
        'pos',
        'samehead',
        'sametail',
        'showboxes',
        'style',
        'tailURL',
        'tail_lp',
        'tailclip',
        'tailhref',
        'taillabel',
        'tailport',
        'tailtarget',
        'tailtooltip',
        'target',
        'tooltip',
        'weight',
        ])

    _validator_overrides = {}

    def __init__(self, **kwargs):
        Attributes.__init__(self, **kwargs)
