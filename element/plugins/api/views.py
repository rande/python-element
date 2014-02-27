import json, base64
import datetime
import element
import flask

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

class CrudView(object):
    def build_js_response(self, data, context):
        flask = context.settings['flask']

        response = flask.make_response(data)
        response.headers['Content-Type'] = 'application/script'        

        return response

    def build_json_response(self, data, context):
        flask = context.settings['flask']

        response = flask.make_response(json.dumps(data, default=date_handler))
        response.headers['Content-Type'] = 'application/json'        

        return response

    def get_method(self, method, format):
        function = ("%s_%s" % (method, format)).lower()

        if hasattr(self, function):
            return getattr(self, function)

        function = ("%s" % method).lower()

        if hasattr(self, function):
            return getattr(self, function)

        return None

    def execute(self, context, *args, **kwargs):
        flask = context.settings['flask']

        # @todo : deal with content negociation
        if kwargs['_format'] not in ['json', 'js']:
            flask.abort(500)

        f = self.get_method(flask.request.method, kwargs['_format'])
        if not f:
            flask.abort(500)

        data, status_code = f(context, *args, **kwargs)
        
        if kwargs['_format'] == 'js':
            response = self.build_js_response(data, context)
        else:
            response = self.build_json_response(data, context)

        response.status_code = status_code

        return response

class ApiView(object):
    def serialize_node(self, node):
        return {
            'id': base64.encodestring(node.id).strip(),
            'path': node.id,
            'type': node.type,
            'data': node.data,
        }

    def serialize_handler(self, handler):
        return {
            'code': handler.code,
            'name': handler.get_name()
        }

class ListView(ApiView, CrudView):
    def __init__(self, node_manager):
        self.node_manager = node_manager

    def get(self, context, path, **kwargs):
        data = {
            'next': '',
            'previous': '',
            'self': '',
            'path': path,
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

        for node in self.node_manager.get_nodes(path=path, limit=limit, offset=offset):
            data['results'].append(self.serialize_node(node))

        return data, 200

class NodeView(ApiView, CrudView):
    def __init__(self, node_manager):
        self.node_manager = node_manager

    def get_node(self, path):
        return self.node_manager.get_node(base64.decodestring(path))
        
    def get(self, context, path, **kwargs):
        node = self.get_node(path)

        if not node:
            return {}, 404

        return self.serialize_node(self.get_node(path)), 200

    def post(self, context, path, **kwargs):
        node = self.get_node(path)

        if node:
            return {}, 202

        flask = context.settings['flask']

        data = json.loads(flask.request.data)

        id = base64.decodestring(path)

        node = element.node.Node(id, data['type'], data['data'])

        self.node_manager.save(node)

        return self.serialize_node(node), 200

    def put(self, context, path, **kwargs):
        node = self.get_node(path)

        if not node:
            return {}, 404

        flask = context.settings['flask']

        node = json.loads(flask.request.data)       
        node['id'] = base64.decodestring(path)

        node = element.node.Node(node['id'], node['type'], node['data'])

        self.node_manager.save(node)

        return self.serialize_node(node), 200

    def delete(self, context, path, **kwargs):
        node = self.get_node(path)

        if not node:
            return {}, 404

        if self.node_manager.delete_node(node):
            return {}, 200
        else:
            return {}, 500

class HandlerView(CrudView, ApiView):
    def __init__(self, node_manager, locator):
        self.node_manager = node_manager
        self.locator = locator

    def get(self, context, code, **kwargs):
        return self.serialize_handler(self.node_manager.handlers[code])

    def get_js(self, context, code, **kwargs):

        handler = self.node_manager.handlers[code]

        filecode = "element:%s/static/js/handler.js" % code

        try:
            filename = self.locator.locate(filecode)
            f = file(filename, 'r')
            content = f.read()
            f.close()
        except:
            content = "// the ressource: %s does not exist" % filecode;

        return """
/**
 * This javascript is rendered dynamically by the node handler.
 * To change this code, you need to create a proper js file in the ressource 
 * folder
 *
 * handler: %s - %s
 **/
 %s
 ;
 """ % (handler.code, handler.get_name(), content), 200

class HandlerListView(CrudView, ApiView):
    def __init__(self, node_manager):
        self.node_manager = node_manager

    def get(self, context, **kwargs):
        data = {
            'next': '',
            'previous': '',
            'self': '',
            'results': []
        }

        for name, handler in self.node_manager.handlers.iteritems():
            data['results'].append(self.serialize_handler(handler))

        return data, 200