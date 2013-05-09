from flask.views import MethodView, View
import flask

class PathView(MethodView):
    def __init__(self, node_manager, context_creator, event_dispatcher):
        self.node_manager = node_manager
        self.context_creator = context_creator
        self.event_dispatcher = event_dispatcher

    def post(self, path):
        return self.get(path)

    def get(self, path):
        # load the node
        node = self.get_node(path)
        
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
