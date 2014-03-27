# vim: set fileencoding=utf-8 :
import unittest
from element.plugins.node.standardize import Standardizer
from element.node import Node
import datetime
class StandardizeTest(unittest.TestCase):

    def setUp(self):
        self.standardizer = Standardizer()

    def test_normalize(self):

        self.maxDiff = 2048

        node = Node("uuid", {
            'created_at': datetime.datetime(2014, 3, 27, 9, 0, 45, 577699),
            'updated_at': datetime.datetime(2014, 3, 27, 9, 0, 45, 577747),
            'published_at': datetime.datetime(2014, 3, 27, 9, 1, 56, 61007),
        })

        self.standardizer.normalize(node)

        expected = {
            'status': 0,
            'set': None,
            'set_uuid': None,
            'deleted': False,
            'type': None,
            'created_at': datetime.datetime(2014, 3, 27, 9, 0, 45, 577699),
            'enabled': True,
            'updated_at': datetime.datetime(2014, 3, 27, 9, 0, 45, 577747),
            'weight': 0,
            'current': True,
            'manager': None,
            'version': 1,
            'path': None,
            'revision': 1,
            'category': False,
            'copyright': False,
            'tags': [],
            'title': 'No title defined',
            'content': False,
            'published_at': datetime.datetime(2014, 3, 27, 9, 1, 56, 61007),
            'authors': [],
            'response': {'status_code': None, 'Cache-Control': ['no-cache']},
            'id': None,
            'uuid': 'uuid'
        }

        self.assertEquals(expected, node.all())
