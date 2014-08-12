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

from element.plugins.profiler import Run
from tornado.web import RequestHandler, Application
from tornado.httpserver import HTTPRequest
from element.plugins.profiler.pycallgraph import PyCallgraphCollector
from element.plugins.node.jinja import get_dummy_connection

import os, shutil

current_path = os.path.dirname(os.path.realpath(__file__))

class PyCallgraphCollectorTest(unittest.TestCase):
    def test_run(self):

        app = Application()
        request = HTTPRequest('GET', '/', connection=get_dummy_connection())

        handler = RequestHandler(app, request)
        handler.run = Run()

        shutil.rmtree('/tmp/python-element/', ignore_errors=True)

        path = "/tmp/python-element//%s" % handler.run.id

        os.makedirs(path)

        p = PyCallgraphCollector('/tmp/python-element/')
        p.on_request(handler, handler.run)

        self.assertIsInstance(handler.run, Run)

        p.on_terminate(handler, handler.run)

        self.assertTrue(os.path.isfile('/tmp/python-element/%s/pycallgraph.dot' % handler.run.id))
