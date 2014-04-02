from tests.functionals import AuthAsyncHTTPTestCase

class FunctionTest(AuthAsyncHTTPTestCase):

    def assert_json(self, response):
        self.assertEquals(200, response.code)
        self.assertEquals('application/json', response.headers['Content-Type'])

        return self

    def test_handlers(self):
        response = self.get('/feeds/python.rss')
        self.assertEquals('application/rss+xml', response.headers['Content-Type'])

        response = self.get('/feeds/python.atom')
        self.assertEquals('application/atom+xml', response.headers['Content-Type'])