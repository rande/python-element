# vim: set fileencoding=utf-8 :
import unittest
import element.node
from element.manager import is_uuid, get_uuid
import os
import ioc.event
import element.loaders
import mock 
import datetime

class NodeManagerTest(unittest.TestCase):
    def setUp(self):

        fs = element.manager.fs.FsManager(
            "%s/fixtures/" % os.path.dirname(os.path.abspath(__file__)),
            element.loaders.YamlNodeLoader()
        )

        fs.build_references()

        self.manager = element.node.NodeManager(fs, ioc.event.Dispatcher())

    def test_get_node(self):
        self.assertIsNone(self.manager.get_node('fake'))

        node = self.manager.get_node('29742dd8-e12c-2f49-961dfdda')

        self.assertIsInstance(node, element.node.Node)
        self.assertEquals("My Post Content", node.title)
        self.assertEquals("blog.post", node.type)
        self.assertIsNotNone(node.content)

    def test_event(self):
        dispatch = mock.Mock()
        dispatch.return_value = ioc.event.Event({
            'node': element.node.Node(get_uuid('id'), {"type": "mytype"})
        })

        self.manager.event_dispatcher.dispatch = dispatch

        node = self.manager.get_node('29742dd8-e12c-2f49-961dfdda')

        self.assertIsInstance(node, element.node.Node)

        self.assertTrue(dispatch.called)

    def test_create_node(self):
        node = element.node.Node('test')

        self.assertEquals('test', node.uuid)
        self.assertIsNotNone(node.uuid)

        node = element.node.Node(get_uuid('hello'), {
            'extra': 'salut',
        })

        self.assertEquals('2cf24dba-5fb0-a30e-26e83b2a', node.uuid)
        self.assertEquals(1, node.revision)
        self.assertEquals(1, node.version)
        self.assertEquals(0, node.weight)
        self.assertTrue(node.enabled)
        self.assertTrue(node.current)
        self.assertFalse(node.deleted)
        self.assertIsNone(node.type)
        self.assertIsNone(node.set_uuid)
        self.assertIsNone(node.set)
        self.assertEquals({'extra': 'salut'}, node.data)

    def test_node_all(self):
        node = element.node.Node(get_uuid('hello'), {
            'id': 'hello',
            'extra': 'salut',
            'created_at': datetime.datetime(2014, 3, 25, 6, 12, 34, 615072),
            'updated_at': datetime.datetime(2014, 3, 25, 6, 12, 34, 615072),
        })

        expected = {
            'id': 'hello',
            'manager': None,
            'revision': 1,
            'status': 0,
            'set': None,
            'path': None,
            'set_uuid': None,
            'extra': 'salut',
            'deleted': False,
            'created_at': datetime.datetime(2014, 3, 25, 6, 12, 34, 615072),
            'updated_at': datetime.datetime(2014, 3, 25, 6, 12, 34, 615072),
            'current': True,
            'data': {'extra': 'salut'},
            'enabled': True,
            'type': None,
            'version': 1,
            'weight': 0
        }

        self.assertEquals(expected, node.all())