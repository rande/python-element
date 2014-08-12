#
# Copyright 2014 Thomas Rabaix <thomas.rabaix@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

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
