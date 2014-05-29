from tests.functionals import AuthAsyncHTTPTestCase

class TalksTest(AuthAsyncHTTPTestCase):
    def test_handlers(self):
        response = self.get('/talks/what-is-python-element')

        self.assertIn("This talk is a small demo", response.body)
