import unittest, os, sys
from tornado.testing import AsyncHTTPTestCase
import json

base = sys.path[0]
sys.path.insert(0, base + "/../../../")
sys.path.insert(0, base + "/../../../../../")

from start import get_container

import element
from element.manager import get_uuid

parameters = {
    'ioc.debug': True,
    'ioc.env': 'prod',
    'project.root_folder': os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../..')
}

application = get_container(parameters).get("ioc.extra.tornado.application")

class AuthAsyncHTTPTestCase(AsyncHTTPTestCase):
    def do_fetch(self, url, **kwargs):
        kwargs['auth_username'] = 'admin'
        kwargs['auth_password'] = 'admin'

        return self.fetch(url, **kwargs)

    def get(self, url, **kwargs):
        return self.do_fetch(url, **kwargs)

    def delete(self, url, **kwargs):
        return self.do_fetch(url, method="DELETE", **kwargs)

    def put_json(self, url, data, **kwargs):
        kwargs['headers'] = {'Content-Type': 'application/json'}

        response = self.do_fetch(url, method="PUT", body=json.dumps(data), **kwargs)

        return response, json.loads(response.body)

    def post_json(self, url, data, **kwargs):
        kwargs['headers'] = {'Content-Type': 'application/json'}

        response = self.do_fetch(url, method="POST", body=json.dumps(data), **kwargs)

        return response, json.loads(response.body)

    def delete_json(self, url, **kwargs):
        kwargs['headers'] = {'Content-Type': 'application/json'}

        response = self.do_fetch(url, method="DELETE", **kwargs)

        return response, json.loads(response.body)

class FunctionTest(AuthAsyncHTTPTestCase):

    def get_app(self):
        return application

    def assert_json(self, response):
        self.assertEquals(200, response.code)
        self.assertEquals('application/json', response.headers['Content-Type'])

        return self

    def test_handlers(self):
        response = self.get('/api/element/handlers.json')

        self.assert_json(response)

        body = json.loads(response.body)

        self.assertEquals(13, len(body['results']))

    def test_node_list(self):
        response = self.get('/api/element/node.json')

        self.assert_json(response)

    def test_node_get(self):
        # 41447798-d348-5885-d856f6cb => favicon.ico
        response = self.get('/api/element/node/41447798-d348-5885-d856f6cb.json')

        self.assert_json(response)

    def test_node_get_error(self):
        response = self.get('/api/element/node/41447798-fake-5885-d856f6cb.json')

        self.assertEquals(404, response.code)
        self.assertEquals('application/json', response.headers['Content-Type'])

    def test_delete_with_error(self):
        response = self.delete('/api/element/node/41447798-fake-5885-d856f6cb.json', **{
            'headers': {'Content-Type': 'application/json'}
        })

        self.assertEquals(404, response.code)
        self.assertEquals('application/json', response.headers['Content-Type'])

    def test_node_put(self):
        # 093e7d5f-dbaa-cfa9-2448861b => contact
        response, node = self.put_json('/api/element/node/093e7d5f-dbaa-cfa9-2448861b.json', {
            "path": "contact",
            "type": "contact.form",
            "manager": "fs",
            "category": False,
            "title": "Contact",
            "created_at": "2013-07-13T00:28:18.567442",
            "enabled": True,
            "content": False,
            "published_at": "2013-07-13T00:28:18.567451",
            "email": {
                "to": "an-email@localhost",
                "from": "no-reply@localhost",
                "subject": "Contact Form localhost"
            }
        })

        self.assertEquals(200, response.code)
        self.assertEquals('application/json', response.headers['Content-Type'])
        self.assertEquals("contact", node['path'])
        self.assertEquals("Contact", node['title'])

    def test_node_post_and_delete(self):
        # 562f2833-d589-8890-becf31b0 => test-node
        response = self.get('/api/element/node/562f2833-d589-8890-becf31b0.json')

        if response.code == 200:
            # node exist ... last test fail ?
            response = self.delete('/api/element/node/562f2833-d589-8890-becf31b0.json')

            self.assertEquals(200, response.code)

        response, node = self.post_json('/api/element/node/none.json', {
            'type': 'blog.post',
            'slug': 'test-node',
            'path': 'test-node',
            'manager':  'fs',
            'content':  'This is a blog post',
            'format':   'markdown'
        })

        self.assertEquals(200, response.code)
        self.assertEquals('application/json', response.headers['Content-Type'])
        self.assertEquals("test-node", node['path'])