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

import markdown
from docutils.core import publish_parts
import json
import element.node
import jinja2

class Formatter(object):

    def format(self, content, formatter='markdown'):

        if formatter == 'markdown':
            return markdown.markdown(content, ['tables', 'codehilite', 'fenced_code'])

        elif formatter in ['rst', 'sphinx']:
            parts = publish_parts(content, writer_name='html', settings_overrides={
                'input_encoding': 'unicode',
                'output_encoding': 'unicode',
                'syntax_highlight': 'short',
            })

            return parts['html_body']
        elif formatter == 'json':
            return json.dump(content)

        return content

    def unicode(self, content):
        if isinstance(content, unicode):
            return content

        return content.decode("utf-8")

    def markup(self, content, format=None):
        if isinstance(content, element.node.NodeContext):
            format = content.node.format
            content = content.node.content

        if isinstance(content, element.node.Node):
            format = content.format
            content = content.content

        return self.unicode(self.format(content, formatter=format))

    def render_jinja_block(self, template, block_name, parameters):
        """
        render a specific jinja block
        """
        content = ""

        if block_name not in template.blocks:
            return content

        block = template.blocks[block_name]

        for block_content in block(template.new_context(parameters)):
            content += block_content

        return jinja2.Markup(content)
