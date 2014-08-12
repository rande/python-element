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
import re
from element.plugins.security.firewall import AccessMap, FirewallMap, Firewall
from element.plugins.security.exceptions import AccessDeniedException
from element.plugins.security.handler import AnonymousAuthenticationHandler
from element.plugins.security.security import SecurityContext

from element.plugins.node.jinja import get_dummy_connection
from tornado.httpserver import HTTPRequest
from tornado.web import Application

from ioc.extra.tornado.handler import BaseHandler


from ioc.event import Event


class AccesMapTest(unittest.TestCase):
    def test_match(self):
        map = AccessMap([
            (re.compile("/admin/.*"), 'admin'),
            (re.compile("/blog/.*"), ['anonymous'])
        ])

        paths = [
            ('/admin/dashboard', ['admin']),
            ('/', None),
            ('/blog/2012', ['anonymous'])
        ]

        for path, expected in paths:
            self.assertEquals(expected, map.get_pattern(HTTPRequest("GET", path, connection=get_dummy_connection())))

class FirewallMapTest(unittest.TestCase):
    def test_map(self):
        map = FirewallMap([
            (re.compile("/admin/.*"), ([], None)),
            (re.compile("/blog/.*"), ([], None))
        ])

        paths = [
            ('/admin/dashboard', ([], None)),
            ('/', ([], None)),
            ('/blog/2012', ([], None))
        ]

        for path, expected in paths:
            self.assertEquals(expected, map.get_context(HTTPRequest("GET", path, connection=get_dummy_connection())))

class FirewallTest(unittest.TestCase):
    def test_get_context_with_no_valid_context(self):
        f = Firewall(FirewallMap())

        rq = BaseHandler(Application(), HTTPRequest("GET", "/", connection=get_dummy_connection()))

        with self.assertRaises(AccessDeniedException):
            f.onRequest(Event({
                'request': rq.request,
                'request_handler': rq
            }))

    def test_get_context_with_empty_listeners(self):
        f = Firewall(FirewallMap([
            (re.compile("/admin/.*"), ([], None)),
        ]))

        rq = BaseHandler(Application(), HTTPRequest("GET", "/admin/dashboard", connection=get_dummy_connection()))

        with self.assertRaises(AccessDeniedException):
            f.onRequest(Event({
                'request': rq.request,
                'request_handler': rq
            }))

    def test_get_context_with_valid_listeners(self):
        c = SecurityContext()
        f = Firewall(FirewallMap([
            (re.compile("/admin/.*"), ([
                AnonymousAuthenticationHandler('key', c),
            ], None)),
        ]))

        rq = BaseHandler(Application(), HTTPRequest("GET", "/admin/dashboard", connection=get_dummy_connection()))

        e = Event({
            'request': rq.request,
            'request_handler': rq
        })
        f.onRequest(e)

        self.assertIsNotNone(c.token)

