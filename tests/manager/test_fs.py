# vim: set fileencoding=utf-8 :
import unittest
import ioc.event
import element.manager.fs
import element.loaders
import os

class FsManagerTest(unittest.TestCase):     
    def test(self):

        loader = element.loaders.YamlNodeLoader()
        
        path = "%s/../fixtures/data/" % os.path.dirname(os.path.abspath(__file__))

        fs = element.manager.fs.FsManager(path, loader)

        cases = [
            ({'path': "/../private"}, 0),
            ({}, 1),
            ({'type': 'blog.post'}, 1),
            ({'type': 'fake'}, 0),
            ({'type': 'fake', 'types': ['blog.post']}, 1),
            ({'types': ['blog.post', 'fake']}, 1),
            ({'types': [], 'tags': ['red', 'yellow']}, 1),
            ({'types': [], 'tags': ['red', 'yellow', 'brown']}, 0),
            ({'types': [], 'tags': []}, 1)
        ]

        for kwarg, expected in cases:
            nodes = fs.find(**kwarg)
            self.assertEquals(expected, len(nodes))
