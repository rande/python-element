# vim: set fileencoding=utf-8 :
import unittest
import ioc.event
import element.manager.fs
import element.loaders
import os

class TestFsManager(unittest.TestCase):     
    def test(self):

        loader = element.loaders.LoaderChain()
        
        path = "%s/../fixtures/" % os.path.dirname(os.path.abspath(__file__))
        
        fs = element.manager.fs.FsManager(path, loader)

        fs.find()
        