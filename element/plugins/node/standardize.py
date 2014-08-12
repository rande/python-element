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

import ioc.event
import dateutil.parser
import datetime

class Standardizer(object):
    def normalize_node(self, event):
        node = event.get('node')
        self.normalize(node)

    def normalize_nodes(self, event):
        for node in event.get('nodes'):
            self.normalize(node)

    def normalize(self, node):
        """
        Normalize node to make sure the default fields are set properly
        """

        if 'published_at' not in node.data or not node.data['published_at']:
            node.data['published_at'] = datetime.datetime.now()

        if not isinstance(node.data['published_at'], datetime.datetime):
            node.data['published_at'] = dateutil.parser.parse(node.data['published_at'])

        if 'content' not in node.data:
            node.data['content'] = False

        if 'title' not in node.data:
            node.data['title'] = "No title defined"

        if 'tags' not in node.data:
            node.data['tags'] = []

        if 'category' not in node.data:
            node.data['category'] = False

        if 'authors' not in node.data:
            node.data['authors'] = []

        if 'copyright' not in node.data:
            node.data['copyright'] = False

        if 'response' not in node.data:
            node.data['response'] = {}

        defaults = {
            'status_code': None,
            'Cache-Control': [
                'no-cache'
            ],
        }

        defaults.update(node.data['response'])

        node.data['response'] = defaults

        if not node.manager and 'manager' in node.data:
            node.manager = node.data['manager']

    def render_response(self, event):
        event.get('request_handler').set_header('X-Content-Generator', 'Python Element - Thomas Rabaix - http://github.com/rande/python-element')
