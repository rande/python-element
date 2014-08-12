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
from element.exceptions import PerformanceException

class TemplateHandler(element.node.NodeHandler):
    def __init__(self, node_manager):
        self.node_manager = node_manager

    def get_name(self):
        return 'Node Template'

    def get_defaults(self, node):
        return {
            'template': node.template,
        }

    def execute(self, request_handler, context):
        return 200,  context.settings['template'], {
            'context': context,
        }

class IndexHandler(element.node.NodeHandler):
    def __init__(self, node_manager):
        self.node_manager = node_manager

    def get_name(self):
        return 'Node Index'

    def get_defaults(self, node):
        if 'filters' not in node.data:
            node.data['filters'] = {}

        if 'types' not in node.data['filters']:
            node.data['filters']['types'] = []

        if 'tags' not in node.data['filters']:
            node.data['filters']['tags'] = []

        if 'category' not in node.data['filters']:
            node.data['filters']['category'] = None

        if 'path' not in node.data['filters']:
            node.data['filters']['path'] = None

        if 'limit' not in node.data['filters']:
            node.data['filters']['limit'] = 64

        if 'offset' not in node.data['filters']:
            node.data['filters']['offset'] = 0

        node.data['filters']['limit'] = int(node.data['filters']['limit'])
        node.data['filters']['offset'] = int(node.data['filters']['offset'])

        return {
            'template': self.get_base_template(node),
        }

    def get_base_template(self, node):
        return node.template or 'element.plugins.node:index.html'

    def execute(self, request_handler, context):
        if context.filters['limit'] > 128:
            raise PerformanceException("The limit cannot be greater than 128 (limit:%s)" % context.filters['limit'])

        nodes = self.node_manager.get_nodes(**{
            'types':    context.filters['types'], 
            'limit':    context.filters['limit'], 
            'offset':   context.filters['offset'], 
            'category': context.filters['category'], 
            'tags':     context.filters['tags'], 
            'path':     context.filters['path'],
        })

        nodes.sort(key=lambda node: node.data['published_at'], reverse=True)

        return 200, context.settings['template'], {
            'context': context,
            'nodes': nodes
        }