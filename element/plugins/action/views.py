import element.node

from element.views import Dispatcher

class ActionView(Dispatcher):
    def dispatch(self, request_handler, *args, **kwargs):
        if '_controller' not in kwargs:
            return

        serviceId, method = kwargs['_controller'].split(":")

        del kwargs['_controller']

        parameters = request_handler.request.query_arguments.copy()
        parameters.update(kwargs)

        node = element.node.Node('action://%s' % serviceId, {
            'type': 'action.node',
            'serviceId': serviceId,
            'method': method,
            'kwargs': parameters,
            'request': request_handler.request
        })

        event = self.event_dispatcher.dispatch('element.node.load.success', {
            'node': node
        })

        return self._execute(request_handler, event.get('node'))
