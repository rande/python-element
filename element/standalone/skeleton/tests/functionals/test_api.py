import unittest, os, sys
from webtest import TestApp

base = sys.path[0]
sys.path.insert(0, base + "/../../")
sys.path.insert(0, base + "/../../../../../")

from start import get_container

import element

parameters = {
    'ioc.debug': True,
    'ioc.env': 'prod',
    'project.root_folder': os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../..')
}

app = TestApp(get_container(parameters).get("ioc.extra.flask.app"))

class FunctionTest(unittest.TestCase):
    def assert_json(self, response):
        self.assertEquals(200, response.status_int)
        self.assertEquals('application/json', response.content_type)

        return self

    def test_handlers(self):
        response = app.get('/api/element/handlers.json')

        self.assert_json(response)

        self.assertEquals(13, len(response.json['results']))

    def test_node_list(self):
        response = app.get('/api/element/node.json')

        self.assert_json(response)

    def test_node_get(self):
        response = app.get('/api/element/node/ZmF2aWNvbi5pY28=.json')

        self.assert_json(response)

    def test_node_get_error(self):
        response = app.get('/api/element/node/L2Zha2UtcGFnZQ==.json', expect_errors=True)

        self.assertEquals(404, response.status_int)
        self.assertEquals('application/json', response.content_type)

    def test_delete_with_error(self):
        response = app.delete_json('/api/element/node/L2Zha2UtcGFnZQ==.json', expect_errors=True)

        self.assertEquals(404, response.status_int)
        self.assertEquals('application/json', response.content_type)

    def test_node_put(self):
        response = app.put_json('/api/element/node/Y29udGFjdA==.json', {
            "path": "contact", 
            "type": "contact.form", 
            "id": "Y29udGFjdA==", 
            "data": {
                "category": False, 
                "title": "Contact", 
                "created_at": "2013-07-13T00:28:18.567442", 
                "enabled": True, 
                "content": False, 
                "published_at": "2013-07-13T00:28:18.567451", 
                "type": "contact.form", 
                "email": {
                    "to": "an-email@localhost", 
                    "from": "no-reply@localhost", 
                    "subject": "Contact Form localhost"
                }
            }
        })

        self.assert_json(response)

        self.assertEquals("contact", response.json['path'])
        self.assertEquals("Contact", response.json['data']['title'])

    def test_node_post_and_delete(self):
        # dGVzdC1ub2Rl => /test-node.json
        response = app.get('/api/element/node/dGVzdC1ub2Rl.json', expect_errors=True)

        if response.status_int == 200:
            # node exist ... last test fail ?
            response = app.delete_json('/api/element/node/dGVzdC1ub2Rl.json')

        response = app.post_json('/api/element/node/dGVzdC1ub2Rl.json', {
            'type': 'blog.post',
            'data': {
                'content': 'This is a blog post',
                'format': 'markdown'
            }
        })
