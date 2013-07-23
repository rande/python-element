# vim: set fileencoding=utf-8 :
import unittest
import element.plugins.blog.blog
import os

class PostHandlerTest(unittest.TestCase):     
    def test_init(self):
        handler = element.plugins.blog.blog.PostHandler()
        