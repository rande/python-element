# vim: set fileencoding=utf-8 :
import unittest

from element.plugins.profiler import Run, Profiler, ProfilerListener
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

        r.add_metric('request', expected)

        self.assertEquals(expected, r.get_metric('request'))
        self.assertNotEqual(None, r.id)


class ProfilerTest(unittest.TestCase):
    def test_init(self):
        p = Profiler('/tmp/python-element/', None)

        run = p.create_run()

        self.assertNotEqual(run.id, None)

    def test_save_and_load(self):
        p = Profiler('/tmp/python-element/', None)

        run = p.create_run()

        p.store_run(run)

        saved_run = p.load_run(run.id)

        self.assertEquals(saved_run.id, run.id)


