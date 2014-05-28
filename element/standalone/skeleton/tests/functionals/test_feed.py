from tests.functionals import AuthAsyncHTTPTestCase

class FunctionTest(AuthAsyncHTTPTestCase):
    def test_handlers(self):
        response = self.get('/feeds/python.rss')
        self.assertEquals('application/rss+xml', response.headers['Content-Type'])

        response = self.get('/feeds/python.atom')
        self.assertEquals('application/atom+xml', response.headers['Content-Type'])