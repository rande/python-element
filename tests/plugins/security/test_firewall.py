# vim: set fileencoding=utf-8 :
import unittest
import re
from element.plugins.security.firewall import AccessMap, FirewallMap, Firewall
from element.plugins.security.exceptions import AccessDeniedException
from element.plugins.security.handler import AnonymousAuthenticationHandler
from element.plugins.security.security import SecurityContext

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
            self.assertEquals(expected, map.get_pattern(HTTPRequest("GET", path)))

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
            self.assertEquals(expected, map.get_context(HTTPRequest("GET", path)))

class FirewallTest(unittest.TestCase):
    def test_get_context_with_no_valid_context(self):
        f = Firewall(FirewallMap())

        rq = BaseHandler(Application(), HTTPRequest("GET", "/"))

        with self.assertRaises(AccessDeniedException):
            f.onRequest(Event({
                'request': rq.request,
                'request_handler': rq
            }))

    def test_get_context_with_empty_listeners(self):
        f = Firewall(FirewallMap([
            (re.compile("/admin/.*"), ([], None)),
        ]))

        rq = BaseHandler(Application(), HTTPRequest("GET", "/admin/dashboard"))

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

        rq = BaseHandler(Application(), HTTPRequest("GET", "/admin/dashboard"))

        e = Event({
            'request': rq.request,
            'request_handler': rq
        })
        f.onRequest(e)

        self.assertIsNotNone(c.token)

