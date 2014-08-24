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
import element.views, element.context
from element.manager import is_uuid, get_uuid
import os
import ioc.event
import element.loaders
import mock
import datetime

class NodeRendererTest(unittest.TestCase):
    def setUp(self):
        self.dispatcher = mock.Mock()
        self.node_manager = mock.Mock()
        self.request_handler = mock.Mock()
        self.node_handler = mock.Mock()
        self.context_creator = mock.Mock()

    def test_render_with_no_main_handler_and_no_listener(self):
        event = mock.Mock()
        event.has.return_value = False

        self.dispatcher.dispatch.return_value = event
        self.node_manager.get_handler.return_value = None

        node = mock.Mock()

        renderer = element.views.NodeRenderer(self.node_manager, self.context_creator, self.dispatcher)
        renderer.render(self.request_handler, node)

        self.dispatcher.dispatch.assert_called()
        self.node_manager.get_handler.assert_called()
        self.request_handler.set_status.assert_called_with(500)

        event.has.assert_called_with('node')

    def test_render_with_no_main_handler_and_with_listener_and_with_no_valid_sub_handler(self):
        event = mock.Mock()
        event.has.return_value = True
        event.get.return_value = mock.Mock()

        self.dispatcher.dispatch.return_value = event
        self.node_manager.get_handler.return_value = None

        node = mock.Mock()

        renderer = element.views.NodeRenderer(self.node_manager, self.context_creator, self.dispatcher)
        renderer.render(self.request_handler, node)

        self.dispatcher.dispatch.assert_called()
        self.node_manager.get_handler.assert_called()
        self.request_handler.set_status.assert_called_with(500)
        event.has.assert_called_with('node')

    def test_render_with_main_handler(self):
        event = mock.Mock()
        event.has.return_value = False

        context = mock.Mock()

        self.dispatcher.dispatch.return_value = event
        self.node_manager.get_handler.return_value = self.node_handler
        self.context_creator.build.return_value = context
        self.node_handler.execute.return_value = {}

        node = mock.Mock()

        renderer = element.views.NodeRenderer(self.node_manager, self.context_creator, self.dispatcher)
        renderer.render(self.request_handler, node)

        self.dispatcher.dispatch.assert_called()
        self.node_manager.get_handler.assert_called()
        self.node_handler.execute.assert_called_with(self.request_handler, context)