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

class DisqusHandler(element.node.NodeHandler):
    def __init__(self, account, templating):
        self.account = account
        self.templating = templating

    def get_defaults(self, node):
        return {
            'template': 'element.plugins.disqus:comments.html'
        }

    def get_name(self):
        return 'Disqus'

    def execute(self, request_handler, context):
        if not self.account:
            return

        params = {
            'account': self.account,
        }

        self.render(request_handler, self.templating, context.settings['template'], params)

    def listener(self, event):
        node = element.node.Node('disqus://%s' % event.get('subject').id, {
            'type': 'disqus.comments',
        })

        event.set('node', node)