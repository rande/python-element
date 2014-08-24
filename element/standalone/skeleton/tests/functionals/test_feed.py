from tests.functionals import AuthAsyncHTTPTestCase

class FunctionTest(AuthAsyncHTTPTestCase):
    def test_handlers(self):
        response = self.get('/feeds/python.rss')
        self.assertEquals('application/rss+xml', response.headers['Content-Type'])

        response = self.get('/feeds/python.atom')
        self.assertEquals('application/atom+xml', response.headers['Content-Type'])

        # monitoring string
        response = self.get('/feeds')
        self.assertEquals(1, response.body.count('3d0cc310765f0e7b37d8aa315b2fe6b8'))