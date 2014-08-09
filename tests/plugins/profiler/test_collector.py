__author__ = 'rande'

import unittest

from element.plugins.profiler.collector import RequestCollector
from tornado.web import RequestHandler, Application
from tornado.httpserver import HTTPRequest
from element.plugins.profiler import Run
from element.plugins.node.jinja import get_dummy_connection

class RequestCollectorTest(unittest.TestCase):
    def setUp(self):
        self.handler = RequestHandler(Application(), HTTPRequest('GET', '/', connection=get_dummy_connection()))
        self.handler.run = Run()
        self.collector = RequestCollector()

    def test_on_request(self):

        app = Application()
        request = HTTPRequest('POST', '/collector?hello=world', body=b"foo=bar&bar=foo", headers={'Content-Type': 'application/x-www-form-urlencoded'}, connection=get_dummy_connection())

        handler = RequestHandler(app, request)
        handler.run = Run()

        self.collector.on_request(handler, handler.run)

        self.assertEquals({
            'body_arguments': {},
            'cookies': '',
            'headers': {'Content-Type': 'application/x-www-form-urlencoded'},
            'host': '127.0.0.1',
            'method': 'POST',
            'path': '/collector',
            'protocol': 'http',
            'query': 'hello=world',
            'body': 'foo=bar&bar=foo',
            'query_arguments': {'hello': ['world']},
            'remote_ip': '127.0.0.1',
            'uri': '/collector?hello=world',
            'version': 'HTTP/1.0',
            'controller': {'class': False, 'file': False, 'line': False, 'method': False},
            'route': False,
            'status_code': False,
        }, handler.run.get_metric('request'))


    def test_on_callback(self):
        class NodeHandler(object):
            def execute(self):
                pass

        m = {'host': 'localhost'}
        self.handler.run.add_metric('request', m)
        self.collector.on_callback(self.handler, self.handler.run, 'element.home', NodeHandler().execute, {'foo': 'bar'})

        self.assertEqual(m, {
            'controller': {'class': 'tests.plugins.profiler.test_collector.NodeHandler',
            'method': 'execute'},
            'host': 'localhost',
            'route': 'element.home',
            'route_parameters': {'foo': 'bar'}
        })

    def test_on_response(self):

        m = {'host': 'localhost'}
        self.handler.run.add_metric('request', m)
        self.handler.set_status(404) # let's make it useful
        self.collector.on_response(self.handler, self.handler.run)

        self.assertEqual(m, {
            'host': 'localhost',
            'status_code': 404
        })
