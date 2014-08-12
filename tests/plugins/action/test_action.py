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
import ioc.component
import element.node, element.plugins.action.action
import ioc.exceptions
from tornado.web import Application
import tests

class RedirectHandlerTest(unittest.TestCase):
    def setUp(self):
        self.handler = element.plugins.action.action.RedirectHandler("/baseurl")

    def test_get_defaults(self):
        self.assertEquals({}, self.handler.get_defaults({}))

    def test_execute_relative(self):

        context = element.node.NodeContext(
            element.node.Node(None, {'type': 'mytype', 'redirect': 'to', 'path': 'node-path'})
        )

        handler = tests.get_default_handler()

        self.handler.execute(handler, context)

        self.assertEquals(handler.get_status(), 302)
        self.assertEquals(handler.get_header('Location'), '/baseurl/node-path/to')


    def test_execute_absolute(self):

        context = element.node.NodeContext(
            element.node.Node(None, {'type': 'mytype', 'redirect': '/to', 'path': '/'})
        )

        handler = tests.get_default_handler()

        self.handler.execute(handler, context)

        self.assertEquals(handler.get_status(), 302)
        self.assertEquals(handler.get_header('Location'), '/baseurl/to')

    def test_execute_absolute_scheme(self):

        context = element.node.NodeContext(
            element.node.Node(None, {'type': 'mytype', 'redirect': 'http://github.com'})
        )

        handler = tests.get_default_handler()

        self.handler.execute(handler, context)

        self.assertEquals(handler.get_status(), 302)
        self.assertEquals(handler.get_header('Location'), 'http://github.com')

class ActionHandlerTest(unittest.TestCase):
    def setUp(self):
        self.handler = element.plugins.action.action.ActionHandler(
            ioc.component.Container(),
            Application(),
            tests.TemplateEngine()
        )

    def test_non_existant_service(self):
        context = element.node.NodeContext(
            element.node.Node('myid', {'type': 'mytype'})
        )

        handler = tests.get_default_handler()

        self.assertRaises(ioc.exceptions.UnknownService, self.handler.execute, handler, context)


    def test_return_tuple(self):
        context = element.node.NodeContext(
            element.node.Node('myid', {'type': 'mytype', 'serviceId': 'fake', 'method': 'foo'})
        )

        class Fake(element.node.NodeHandler):
            def foo(self, request_context, context, **kwargs):
                return 200, "hello", {}

        handler = tests.get_default_handler()

        self.handler.container.add('fake', Fake())

        self.handler.execute(handler, context)

        self.assertEquals(handler.get_status(), 200)
