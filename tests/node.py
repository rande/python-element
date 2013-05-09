# vim: set fileencoding=utf-8 :
import unittest
import element.node
import os
import ioc.event
import element.loaders

class TestNodeManager(unittest.TestCase):
    def setUp(self):
        self.manager = element.node.NodeManager(element.loaders.LoaderChain(), ioc.event.Dispatcher())

    def test_init(self):
        self.assertFalse(self.manager.get_node('fake'))

        # self.manager.add_handler()
        