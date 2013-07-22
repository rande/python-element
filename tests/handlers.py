# vim: set fileencoding=utf-8 :
import unittest
import element.plugins.blog.blog
import os

class TestPostHandler(unittest.TestCase):     
    def test_init(self):
        handler = element.plugins.blog.blog.PostHandler()
        