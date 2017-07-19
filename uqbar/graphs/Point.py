class Point(object):

    __slots__ = ('x', 'y')

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
