# vim: set fileencoding=utf-8 :
import unittest
import ioc.event
import element.plugins.node.standardize
import element.node
import datetime

class EventTest(unittest.TestCase):     
    def test_normalize(self):
        normalize = element.plugins.node.standardize.Standardize()

        event = ioc.event.Event({
            'node': element.node.Node('id', 'my type', {"published_at": "Wed, 16 Nov 2005 19:26:18"})
        })

        normalize.normalize_node(event)

        self.assertIsInstance(event.get('node'), element.node.Node)
        self.assertTrue(event.get('node').enabled)
        self.assertIsInstance(event.get('node').created_at, datetime.datetime)
        self.assertIsInstance(event.get('node').published_at, datetime.datetime)
        