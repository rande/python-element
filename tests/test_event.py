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
import ioc.event
import element.plugins.node.standardize
import element.node
import datetime

class EventTest(unittest.TestCase):     
    def test_normalize(self):
        normalize = element.plugins.node.standardize.Standardizer()

        event = ioc.event.Event({
            'node': element.node.Node('id', {'type': 'my type', "published_at": "Wed, 16 Nov 2005 19:26:18"})
        })

        normalize.normalize_node(event)

        self.assertIsInstance(event.get('node'), element.node.Node)
        self.assertTrue(event.get('node').enabled)
        self.assertIsInstance(event.get('node').created_at, datetime.datetime)
        self.assertIsInstance(event.get('node').published_at, datetime.datetime)
        