class Color:

    def __init__(self, color):
        self.color = str(color)

    def __repr__(self):
        return '<Color {!r}>'.format(self.color)
