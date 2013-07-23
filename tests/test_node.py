# vim: set fileencoding=utf-8 :
import unittest
import element.node
import os
import ioc.event
import element.loaders
import mock 

class NodeManagerTest(unittest.TestCase):
    def setUp(self):

        fs = element.manager.fs.FsManager(
            "%s/fixtures/" % os.path.dirname(os.path.abspath(__file__)),
            element.loaders.YamlNodeLoader()
        )

        self.manager = element.node.NodeManager(fs, ioc.event.Dispatcher())

    def test_get_node(self):
        self.assertIsNone(self.manager.get_node('fake'))

        node = self.manager.get_node('data/2013/my-post-content')

        self.assertIsInstance(node, element.node.Node)
        self.assertEquals("My Post Content", node.title)
        self.assertEquals("blog.post", node.type)
        self.assertIsNotNone(node.content)

    def test_event(self):
        dispatch = mock.Mock()
        dispatch.return_value = ioc.event.Event({
            'node': element.node.Node("id", "type", {})
        })

        self.manager.event_dispatcher.dispatch = dispatch

        node = self.manager.get_node('data/2013/my-post-content')

        self.assertIsInstance(node, element.node.Node)

        self.assertTrue(dispatch.called)
