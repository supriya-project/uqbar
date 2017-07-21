import unittest
import uqbar.graphs


class TestCase(unittest.TestCase):

    def test_mode(self):
        uqbar.graphs.Attributes(mode='cluster')
        uqbar.graphs.Attributes(mode='edge')
        uqbar.graphs.Attributes(mode='graph')
        uqbar.graphs.Attributes(mode='node')
