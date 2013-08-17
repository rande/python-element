from flask.views import MethodView, View
import flask
import element.node

class Dispatcher(object):
    def render_node(self, node, handler):
        # build the execution context
        context = self.context_creator.build(node, handler)

        # render the response
        event = self.event_dispatcher.dispatch('element.node.render_response', {
            'response': handler.execute(context, flask),
            'context': context,
            'request': flask.request
        })

        return event.get('response')

    def execute(self, node):
        # load the related node's handler
        handler = self.node_manager.get_handler(node)

        if not handler:
            event = self.event_dispatcher.dispatch('element.node.internal_error', {
                'node': path,
                'reason': 'No handler found',
                'status_code': 500
            })

            # no listener to generate a valid node error
            if not event.has('node'):
                flask.abort(500)

            node = event.get('node')

            handler = self.node_manager.get_handler(node)

            # no handler to retrieve a generated node error!!
            if not handler:
                flask.abort(500)

        return self.render_node(node, handler)

class ActionView(MethodView, Dispatcher):
    def __init__(self, node_manager, context_creator, event_dispatcher, container):
        self.node_manager = node_manager
        self.context_creator = context_creator
        self.event_dispatcher = event_dispatcher

    def dispatch(self, *args, **kwargs):
        if '_controller' not in kwargs:
            return

        serviceId, method = kwargs['_controller'].split(":")

        del kwargs['_controller']

        parameters = flask.request.args.to_dict()
        parameters.update(kwargs)

        node = element.node.Node('action://%s' % serviceId, 'node.action', {
            'serviceId': serviceId,
            'method': method,
            'kwargs': parameters,
            'request': flask.request
        })

        event = self.event_dispatcher.dispatch('element.node.load.success', {
            'node': node
        })

        return self.execute(event.get('node'))

class PathView(MethodView, Dispatcher):
    def __init__(self, node_manager, context_creator, event_dispatcher):
        self.node_manager = node_manager
        self.context_creator = context_creator
        self.event_dispatcher = event_dispatcher

    def post(self, path):
        return self.get(path)

    def get(self, path):
        # load the node
        node = self.get_node(path)
        
        return self.execute(node)

    def get_node(self, id):
        node = self.node_manager.get_node(id)

        if not node:
            event = self.event_dispatcher.dispatch('element.node.not_found', {
                'path': id,
                'status_code': 404
            })

            if not event.has('node'): # no error handler defined for the application
                flask.abort(404)

            node = event.get('node')

        return node
