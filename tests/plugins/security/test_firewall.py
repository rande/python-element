# vim: set fileencoding=utf-8 :
import unittest
import re
from element.plugins.security.firewall import AccessMap

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