import element.node

class Dispatcher(object):
    def __init__(self, node_manager, context_creator, event_dispatcher, logger):
        self.node_manager = node_manager
        self.context_creator = context_creator
        self.event_dispatcher = event_dispatcher
        self.logger = logger

    def render_node(self, node, request_handler, node_handler):
        # build the execution context
        context = self.context_creator.build(node, node_handler)

        self.logger.debug("[element.node.Dispatcher] render node: %s with handler: %s" % (node.id, node_handler))

        # render the node
        node_handler.execute(request_handler, context)

        # allow external services to update the request_handler
        self.event_dispatcher.dispatch('element.node.render_response', {
            'context': context,
            'request_handler': request_handler
        })

    def _execute(self, request_handler, node):
        # load the related node's handler
        node_handler = self.node_manager.get_handler(node)

        if not node_handler:
            event = self.event_dispatcher.dispatch('element.node.internal_error', {
                'node': node,
                'reason': 'No handler found',
                'status_code': 500
            })

            # no listener to generate a valid node error
            if not event.has('node'):
                request_handler.set_status(500)

                return

            node = event.get('node')

            node_handler = self.node_manager.get_handler(node)

            # no handler to retrieve a generated node error!!
            if not node_handler:
                request_handler.set_status(500)

                return

        return self.render_node(node, request_handler, node_handler)

class ActionView(Dispatcher):
    def dispatch(self, request_handler, *args, **kwargs):
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

        return self._execute(event.get('node'))

class PathView(Dispatcher):
    def execute(self, request_handler, path):
        # load the node
        node, status_code = self.get_node(path)

        request_handler.set_status(status_code)

        if not node:
            return

        return self._execute(request_handler, node)

    def get_node(self, id):
        node = self.node_manager.get_node(id)

        status_code = 200

        if not node:
            status_code = 404

            event = self.event_dispatcher.dispatch('element.node.not_found', {
                'path': id,
                'status_code': status_code
            })

            if not event.has('node'):  # no error handler defined for the application
                return None, status_code

            node = event.get('node')

        return node, status_code
