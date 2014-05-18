__author__ = 'rande'

import unittest

from element.plugins.profiler.collector import RequestCollector
from tornado.web import RequestHandler, Application
from tornado.httpserver import HTTPRequest
from element.plugins.profiler import Run

class RequestCollectorTest(unittest.TestCase):


    def test_on_request(self):

        app = Application()
        request = HTTPRequest('POST', '/collector?hello=world', body=b"foo=bar&bar=foo", headers={'Content-Type': 'application/x-www-form-urlencoded'})

        handler = RequestHandler(app, request)
        handler.run = Run()


        c = RequestCollector()

        c.on_request(handler, handler.run)

        self.assertEquals(handler.run.get_metric('request'), {
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
            'remote_ip': None,
            'uri': '/collector?hello=world',
            'version': 'HTTP/1.0'
        })