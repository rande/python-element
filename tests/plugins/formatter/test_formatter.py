# vim: set fileencoding=utf-8 :
import unittest
from element.plugins.formatter import Formatter

class FormatterTest(unittest.TestCase):
    def setUp(self):
        self.formmater = Formatter()

    def test_markdown(self):
        content = self.formmater.format('**bold**')

        self.assertEquals("<p><strong>bold</strong></p>", content)

        content = self.formmater.format('**bold**', formatter='markdown')

        self.assertEquals("<p><strong>bold</strong></p>", content)


    def test_rst(self):
        content = self.formmater.format('**bold**', formatter='rst')

        self.assertEquals('<div class="document">\n<p><strong>bold</strong></p>\n</div>\n', content)
