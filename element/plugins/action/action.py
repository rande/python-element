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

from element.node import NodeHandler
from element.plugins.node.jinja import SubRequestHandler
from tornado.httpserver import HTTPRequest
from tornado.httputil import HTTPHeaders

class TornadoActionLoader(object):
    def __init__(self, base_url, router):
        self.base_url = base_url
        self.router = router

    def add_action(self, base_path, settings, container):
        if 'name' not in settings:
            raise Exception('Missing action name')

        if 'type' not in settings:
            settings['type'] = 'action.node'

        if 'path' not in settings:
            settings['path'] = ''

        if 'methods' not in settings:
            settings['methods'] = ['GET']

        if 'defaults' not in settings:
            settings['defaults'] = {}

        if '_controller' not in settings['defaults']:
            raise Exception('_controller key is missing for route %s' % settings['name'])

        service, method = settings['defaults']['_controller'].split(":")

        if settings['type'] == 'action.raw':
            view_func = getattr(container.get(service), method)
        elif settings['type'] == 'action.node':
            view_func = getattr(container.get('element.plugins.node.view.action'), 'dispatch')
        else:
            raise Exception('Invalid action type')

        self.router.add(
            settings['name'],
            self.base_url + base_path + settings['path'],
            view_func=view_func,
            methods=settings['methods'],
            defaults=settings['defaults']
        )

    def load_actions(self, event):
        container = event.get('container')
        node_manager = container.get('element.node.manager')

        self.load_action_node(container, node_manager)
        self.load_collection_node(container, node_manager)

    def load_action_node(self, container, node_manager):
        for node in node_manager.get_nodes(types=['action.node', 'action.raw']):
            self.add_action(node.id, node.data, container)

    def load_collection_node(self, container, node_manager):
        for collection in node_manager.get_nodes(type='action.collection',):
            for name, settings in collection.actions.iteritems():
                settings['name'] = name

                self.add_action(collection.id, settings, container)

class ActionHandler(NodeHandler):
    def __init__(self, container, application, templating):
        self.container = container
        self.application = application
        self.templating = templating
        
    def get_defaults(self, node):
        return {
            'template': 'element.plugins.action:index.html'
        }

    def get_name(self):
        return 'Action'

    def execute(self, request_handler, context):
        service = self.container.get(context.node.serviceId)

        result = getattr(service, context.node.method)(request_handler, context, **(context.node.kwargs or {}))

        if isinstance(result, tuple):
            status_code = 500
            template = None
            params = {}
            headers = {
                'Content-Type': 'text/html; charset=utf-8'
            }

            if len(result) == 3:
                status_code, template, params = result

            if len(result) == 4:
                status_code, template, params, headers = result

            if 'context' not in params:
                params['context'] = context

            self.render(request_handler, self.templating, template, params)

            for name, value in headers.iteritems():
                request_handler.add_header(name, value)

            request_handler.set_status(status_code)

            return None

        return result

class DefaultIndex(object):
    def __init__(self, node_manager):
        self.node_manager = node_manager

    def default_index(self, event):
        """
        Try to find the _index.yml file from the dedicated folder,
        if one is found, then no error will be throw to the user
        """
        node = self.node_manager.get_node("%s/_index" % event.get('path'))

        if not node:
            return

        event.stop_propagation()

        node.id = event.get('path')  # restore a valid id, as this one is virtual

        event.set('node', node)

class RedirectHandler(object):
    def __init__(self, base_url):
        self.base_url = base_url

        if self.base_url[-1] == '/':
             self.base_url = self.base_url[:-1]

    def get_name(self):
        return 'Redirect'

    def get_defaults(self, node):
        return {}

    def execute(self, request_handler, context):
        if 'http://' == context.node.redirect[0:7] or 'https://' == context.node.redirect[0:8]:
            return request_handler.redirect(context.node.redirect)

        if context.node.redirect[0] == '/': # absolute uri
            return request_handler.redirect("%s%s" % (self.base_url, context.node.redirect))

        return request_handler.redirect("%s/%s/%s" % (self.base_url, context.node.path, context.node.redirect))
