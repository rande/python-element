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

import element.node

class PageHandler(element.node.NodeHandler):
    def __init__(self, templating, formatter):
        self.templating = templating
        self.formatter = formatter

    def get_name(self):
        return 'Page'

    def get_defaults(self, node):
        return {
            'template': 'element.plugins.page:default.html'
        }

    def execute(self, request_handler, context):
        self.render(request_handler, self.templating, context.settings['template'], {
            'context': context,
            'content': self.formatter.format(context.node.content, formatter=context.node.format),
        })
