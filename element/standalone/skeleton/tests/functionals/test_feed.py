from tests.functionals import AuthAsyncHTTPTestCase

class FunctionTest(AuthAsyncHTTPTestCase):
    def test_handler_rss(self):
        response = self.get('/feeds/python.rss')
        self.assertEquals('application/rss+xml', response.headers['Content-Type'])
        self.assertEquals(response.headers['Cache-Control'], "public, s-maxage=3600")

    def test_handler_atom(self):
        response = self.get('/feeds/python.atom')
        self.assertEquals('application/atom+xml', response.headers['Content-Type'])

    def test_handler_index(self):
        # monitoring string
        response = self.get('/feeds')
        self.assertEquals(1, response.body.count('3d0cc310765f0e7b37d8aa315b2fe6b8'))

