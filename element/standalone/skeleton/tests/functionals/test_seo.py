from tests.functionals import AuthAsyncHTTPTestCase

class SeoValueTest(AuthAsyncHTTPTestCase):
    def test_handlers(self):
        response = self.get('/')


        self.assertIn("<title>[test] Python element - The Python Element Homepage</title>", response.body)
        self.assertIn('<meta name="description" content="Python Element by Thomas Rabaix ~ A CMS based on Tornado with a bit of &#34;ioc&#34; ;)" />', response.body)

        self.assertIn('<meta name="robots" content="index, follow" />', response.body)
        self.assertIn('<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1, user-scalable=no" />', response.body)
        self.assertIn('<meta property="og:site_name" content="Python Element by Thomas Rabaix" />', response.body)
        self.assertIn('<meta property="og:description" content="A CMS based on Tornado ;)" />', response.body)
        self.assertIn('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />', response.body)

