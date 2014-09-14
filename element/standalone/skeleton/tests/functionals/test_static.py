from tests.functionals import AuthAsyncHTTPTestCase
import json
try:
    from PIL import Image, ImageOps
except ImportError:
    import Image
    import ImageOps
import StringIO

class FunctionTest(AuthAsyncHTTPTestCase):
    def test_handlers(self):
        response = self.get('/gallery/2010/australia/IMG_0003.JPG')

        self.assertEquals(200, response.code)
        self.assertEquals('image/jpeg', response.headers['Content-Type'])

        image = Image.open(StringIO.StringIO(response.body))

        self.assertEquals(image.size[0], 640)
        self.assertEquals(image.size[1], 480)

    def test_fit(self):
        response = self.get('/gallery/2010/australia/IMG_0003.JPG?mf=100,100,0.5,0.5')

        self.assertEquals(200, response.code)
        self.assertEquals('image/jpeg', response.headers['Content-Type'])


        image = Image.open(StringIO.StringIO(response.body))

        self.assertEquals(image.size[0], 100)
        self.assertEquals(image.size[1], 100)

    def test_resize(self):
        response = self.get('/gallery/2010/australia/IMG_0003.JPG?mr=320')

        self.assertEquals(200, response.code)
        self.assertEquals('image/jpeg', response.headers['Content-Type'])

        image = Image.open(StringIO.StringIO(response.body))

        self.assertEquals(image.size[0], 320)
        self.assertEquals(image.size[1], 240)
