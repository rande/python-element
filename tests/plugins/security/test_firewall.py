# vim: set fileencoding=utf-8 :
import unittest
import re
from element.plugins.security.firewall import AccessMap, FirewallMap, Firewall
from element.plugins.security.exceptions import AccessDeniedException
from element.plugins.security.handler import AnonymousAuthenticationHandler
from element.plugins.security.security import SecurityContext

from ioc.event import Event

class Request(object):
    pass

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

        request = Request()

        for path, expected in paths:
            request.path = path
            self.assertEquals(expected, map.get_pattern(request))

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

        request = Request()

        for path, expected in paths:
            request.path = path
            self.assertEquals(expected, map.get_context(request))

class FirewallTest(unittest.TestCase):
    def test_get_context_with_no_valid_context(self):
        f = Firewall(FirewallMap())

        with self.assertRaises(AccessDeniedException):
            f.onRequest(Event({
                'request': Request()
            }))

    def test_get_context_with_empty_listeners(self):
        f = Firewall(FirewallMap([
            (re.compile("/admin/.*"), ([], None)),
        ]))

        r = Request()
        r.path = "/admin/dashboard"

        with self.assertRaises(AccessDeniedException):
            f.onRequest(Event({
                'request': r
            }))

    def test_get_context_with_valid_listeners(self):
        c = SecurityContext()
        f = Firewall(FirewallMap([
            (re.compile("/admin/.*"), ([
                AnonymousAuthenticationHandler('key', c),
            ], None)),
        ]))

        r = Request()
        r.path = "/admin/dashboard"

        e = Event({
            'request': r
        })
        f.onRequest(e)

        self.assertIsNotNone(c.token)

