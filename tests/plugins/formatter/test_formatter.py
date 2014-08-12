#
# Copyright 2014 Thomas Rabaix <thomas.rabaix@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import unittest
from element.plugins.formatter import Formatter

class FormatterTest(unittest.TestCase):
    def setUp(self):
        self.formmater = Formatter()

    def test_markdown(self):
        content = self.formmater.format(u'**bold**')

        self.assertEquals("<p><strong>bold</strong></p>", content)

        content = self.formmater.format(u'**bold**', formatter='markdown')

        self.assertEquals("<p><strong>bold</strong></p>", content)

    def test_rst_with_code(self):
        content = self.formmater.format(u'**bold**', formatter='rst')

        self.assertEquals('<div class="document">\n<p><strong>bold</strong></p>\n</div>\n', content)
