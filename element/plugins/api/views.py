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

import json
import element

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

class CrudView(object):
    def build_js_response(self, request_handler, data):
        request_handler.write(data)
        request_handler.set_header('Content-Type', 'application/script')

    def build_json_response(self, request_handler, data):
        request_handler.write(json.dumps(data, default=date_handler))
        request_handler.set_header('Content-Type', 'application/json')

    def get_method(self, method, format):
        function = ("%s_%s" % (method, format)).lower()

        if hasattr(self, function):
            return getattr(self, function)

        function = ("%s" % method).lower()

        if hasattr(self, function):
            return getattr(self, function)

        return None

    def execute(self, request_handler, **kwargs):
        # @todo : deal with content negociation
        if kwargs['_format'] not in ['json', 'js']:
            request_handler.set_status(500)

        f = self.get_method(request_handler.request.method, kwargs['_format'])

        if not f:
            request_handler.set_status(500)
            return

        status_code, data = f(request_handler, **kwargs)

        request_handler.set_status(status_code)

        if kwargs['_format'] == 'js':
            self.build_js_response(request_handler, data)
        else:
            self.build_json_response(request_handler, data)

class ApiView(object):
    def serialize_node(self, node):
        return node.all()

    def serialize_handler(self, handler):
        return {
            'code': handler.code,
            'name': handler.get_name()
        }

class ListView(ApiView, CrudView):
    def __init__(self, node_manager):
        self.node_manager = node_manager

    def get(self, request_handler, **kwargs):
        data = {
            'next': '',
            'previous': '',
            'self': '',
            'path': kwargs['path'],
            'results': []
        }

        limit = 32
        offset = 0

        if "limit" in kwargs:
            limit = int(kwargs["limit"])

        if "offset" in kwargs:
            offset = int(kwargs["offset"])

        if limit > 32 or limit < 0:
            limit = 32

        if offset < 0:
            offset = 0

        for node in self.node_manager.get_nodes(path=kwargs['path'], limit=limit, offset=offset):
            data['results'].append(self.serialize_node(node))

        return 200, data

class NodeView(ApiView, CrudView):
    def __init__(self, node_manager):
        self.node_manager = node_manager

    def get_node(self, uuid):
        return self.node_manager.get_node(uuid)
        
    def get(self, request_handler, **kwargs):
        node = self.get_node(kwargs['uuid'])

        if not node:
            return 404, {}

        return 200, self.serialize_node(node)

    def post(self, request_handler, **kwargs):
        node = self.get_node(kwargs['uuid'])

        if node:
            return 202, {}

        data = json.loads(request_handler.request.body)

        node = element.node.Node(node, data)

        self.node_manager.save(node)

        return 200, self.serialize_node(node)

    def put(self, request_handler, **kwargs):
        node = self.get_node(kwargs['uuid'])

        if not node:
            return 404, {}

        data = json.loads(request_handler.request.body)

        node.define(data)

        self.node_manager.save(node)

        return 200, self.serialize_node(node)

    def delete(self, request_handler, **kwargs):
        node = self.get_node(kwargs['uuid'])

        if not node:
            return 404, {}

        if self.node_manager.delete(node):
            return 200, {}
        else:
            return 500, {}

class HandlerView(CrudView, ApiView):
    def __init__(self, node_manager, locator):
        self.node_manager = node_manager
        self.locator = locator

    def get(self, request_handler, **kwargs):
        return self.serialize_handler(self.node_manager.handlers[kwargs['code']])

    def get_js(self, request_handler, **kwargs):

        handler = self.node_manager.handlers[kwargs['code']]

        filecode = "element:%s/static/js/handler.js" % kwargs['code']

        try:
            filename = self.locator.locate(filecode)

            f = file(filename, 'r')
            content = f.read()
            f.close()
        except:
            content = "// the ressource: %s does not exist" % filecode;

        return 200, """
/**
 * This javascript is rendered dynamically by the node handler.
 * To change this code, you need to create a proper js file in the ressource 
 * folder
 *
 * handler: %s - %s
 **/
 %s
 ;
 """ % (handler.code, handler.get_name(), content)

class HandlerListView(CrudView, ApiView):
    def __init__(self, node_manager):
        self.node_manager = node_manager

    def get(self, request_handler, **kwargs):
        data = {
            'next': '',
            'previous': '',
            'self': '',
            'results': []
        }

        for name, handler in self.node_manager.handlers.iteritems():
            data['results'].append(self.serialize_handler(handler))

        return 200, data