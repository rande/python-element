# vim: set fileencoding=utf-8 :
import unittest
import element.loaders
import element.node
import os

class YamlNodeLoaderTest(unittest.TestCase):
    def setUp(self):
        self.path = "%s/fixtures/data" % os.path.dirname(os.path.abspath(__file__))
        self.loader = element.loaders.YamlNodeLoader()

    def test_init(self):
        self.assertTrue(self.loader.supports("%s/2013/my-post-content.yml" % self.path))
        self.assertFalse(self.loader.supports("%s/2013/fake.yml" % self.path))

        node = self.loader.load("%s/2013/my-post-content.yml" % self.path)

        self.assertEquals("blog.post", node['type'])
        self.assertEquals("My Post Content", node['title'])

        self.assertIsNotNone(node['content'])

class InlineLoaderTest(unittest.TestCase):

    def setUp(self):
        self.loader = element.loaders.InlineLoader()

    def test_support(self):
        self.assertFalse(self.loader.supports([]))
        self.assertFalse(self.loader.supports(''))
        self.assertFalse(self.loader.supports({}))
        self.assertFalse(self.loader.supports({'type': 'hello'}))

        self.assertTrue(self.loader.supports({'type': 'hello', 'id': 'salut'}))

    def test_load(self):
        node = self.loader.load({'type': 'hello', 'id': 'salut'})

        self.assertEquals('hello', node['type'])
        self.assertEquals('salut', node['id'])
