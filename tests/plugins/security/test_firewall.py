# vim: set fileencoding=utf-8 :
import unittest
import re
from element.plugins.security.firewall import AccessMap, FirewallContext, FirewallMap

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

class FirewallContextTest(unittest.TestCase):
    def test_get_context(self):
        f = FirewallContext([])

        self.assertEquals([], f.get_context())

class FirewallMapTest(unittest.TestCase):
    def test_map(self):
        F1 = FirewallContext([])
        F2 = FirewallContext([])

        map = FirewallMap([
            (re.compile("/admin/.*"), F1),
            (re.compile("/blog/.*"), F2)
        ])

        paths = [
            ('/admin/dashboard', F1),
            ('/', None),
            ('/blog/2012', F2)
        ]

        request = Request()

        for path, expected in paths:
            request.path = path
            self.assertEquals(expected, map.get_context(request))

