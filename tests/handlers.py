# vim: set fileencoding=utf-8 :
import unittest
import element.handlers.blog
import os

class TestPostHandler(unittest.TestCase):     
    def test_init(self):
        handler = element.handlers.blog.PostHandler()
        