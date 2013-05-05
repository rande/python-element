# vim: set fileencoding=utf-8 :
import unittest
import element.loaders
import element.node
import os

class TestYamlNodeLoader(unittest.TestCase):
    def setUp(self):
        path = os.path.dirname(os.path.abspath(__file__))

        self.loader = element.loaders.YamlNodeLoader("%s/fixtures/data" % path)

    def test_init(self):
        self.assertTrue(self.loader.supports("2013/my-post-content"))
        self.assertFalse(self.loader.supports("2013/fake"))

        node = self.loader.load("2013/my-post-content")

        self.assertEquals("blog.post", node.type)
        self.assertIsInstance(node, element.node.Node)
        self.assertIsNotNone(node.data)

class TestInlineLoader(unittest.TestCase):

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
        self.assertIsInstance(node, element.node.Node)

        self.assertEquals('hello', node.type)
        self.assertEquals('salut', node.id)
