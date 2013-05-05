# vim: set fileencoding=utf-8 :
import unittest
import ioc.event
import element.event
import element.node
import datetime

class TestEvent(unittest.TestCase):     
    def test_normalize(self):
        event = ioc.event.Event({
            'node': element.node.Node('id', 'my type')
        })

        element.event.normalize_node(event)

        self.assertIsInstance(event.get('node'), element.node.Node)
        self.assertTrue(event.get('node').enabled)
        self.assertIsInstance(event.get('node').created_at, datetime.datetime)
        self.assertIsInstance(event.get('node').published_at, datetime.datetime)
        