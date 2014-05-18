# vim: set fileencoding=utf-8 :
import unittest

from element.plugins.profiler import Run, Profiler
import os

current_path = os.path.dirname(os.path.realpath(__file__))

class RunTest(unittest.TestCase):
    def test_meta(self):
        r = Run()

        expected = {
            'method': 'POST',
            'parameters': {},
            'query_string': {}
        }

        r.add_data('request', expected)

        self.assertEquals(expected, r.get_data('request'))
        self.assertNotEqual(None, r.id)


class ProfilerTest(unittest.TestCase):
    def test_init(self):
        p = Profiler(True, '/tmp/python-element/')