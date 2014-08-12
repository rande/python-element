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
import element.context
import element.node
import mock

class ContextCreatorTest(unittest.TestCase):
    def test_build(self):
        event_dispatcher = mock.Mock()

        creator = element.context.ContextCreator(event_dispatcher)

        handler = mock.Mock()
        handler.get_defaults.return_value = {}

        node = element.node.Node('id', {'type': 'test'})

        context = creator.build(node, handler)

        self.assertIsInstance(context, element.node.NodeContext)
        self.assertEquals(context.node.type, "test")
        self.assertEquals(context.base_template, "element:base.html")
