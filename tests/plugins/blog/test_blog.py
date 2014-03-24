# vim: set fileencoding=utf-8 :
import unittest
import element.plugins.blog.blog

from tests import TemplateEngine

class PostHandlerTest(unittest.TestCase):     
    def test_init(self):
        handler = element.plugins.blog.blog.PostHandler(TemplateEngine())
        