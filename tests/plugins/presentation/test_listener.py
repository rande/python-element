__author__ = 'rande'

import unittest

from element.plugins.presentation.listener import PresentationNode

class PresentationNodeTest(unittest.TestCase):
    def test_slides(self):

        n = PresentationNode('uuid', {
            'content': "slide1\n----\nslide2\n----\nslide3"
        })

        print n.slides()

        self.assertEquals(3, len(n.slides()))