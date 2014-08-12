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


