from tests.functionals import AuthAsyncHTTPTestCase
import json

class FunctionTest(AuthAsyncHTTPTestCase):
    def test_handlers(self):
        response = self.get('/api/element/handlers.json')

        self.assert_json(response)

        body = json.loads(response.body)

        self.assertEquals(16, len(body['results']))

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