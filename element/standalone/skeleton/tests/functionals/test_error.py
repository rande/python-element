from tests.functionals import AuthAsyncHTTPTestCase
import json

class FunctionTest(AuthAsyncHTTPTestCase):
    def test_error_301(self):
        response = self.get('/labs/errors/301', follow_redirects=False)

        self.assertEquals(301, response.code)

    def test_error_404(self):
        response = self.get('/labs/errors/404')

        self.assertEquals(404, response.code)
        self.assertIn("The requested URL was not found on the server", response.body)

    def test_error_500(self):
        response = self.get('/labs/errors/500')

        self.assertEquals(500, response.code)
        self.assertIn("An error occurs while rendering the page", response.body)
