class TornadoActionLoader(object):
    def __init__(self, base_url, router):
        self.base_url = base_url
        self.router = router

    def load_action(self, event):
        container = event.get('container')
        node_manager = container.get('element.node.manager')

        nodes = node_manager.get_nodes(
            type='action.collection', 
            selector=lambda node: now > node.published_at and node.enabled
        )

        for node in nodes:
            for name, settings in node.actions.iteritems():
                if 'methods' not in settings:
                    settings['methods'] = ['GET']

                if 'defaults' not in settings:
                    settings['defaults'] = {}

                if '_controller' not in settings['defaults']:
                    raise Exception('_controller key is missing for route %s' % name)

                service, method = settings['defaults']['_controller'].split(":")

                self.router.add(
                    name,
                    "%s%s%s" % (self.base_url, node.id, settings['path']),
                    view_func=getattr(container.get(service), method),
                    methods=settings['methods'],
                    defaults=settings['defaults']
                )


class ActionHandler(object):
    def __init__(self, container):
        self.container = container
        
    def get_defaults(self, node):
        return {
            'template': 'element.plugins.action:index.html'
        }

    def get_name(self):
        return 'Action'

    def execute(self, context, flask):
        service = self.container.get(context.node.serviceId)

        context.settings['flask'] = flask

        result = getattr(service, context.node.method)(context, **(context.node.kwargs or {}))

        # the service return a response nothing to do ...
        if isinstance(result, flask.Response): 
            return result

        if isinstance(result, tuple):
            template, params = result
            return flask.make_response(flask.render_template(template, **params))

        return flask.make_response(flask.render_template(context.settings['template'], **{
            'context': context,
            'content': result
        }))

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

        node.id = event.get('path') # restore a valid id, as this one is virtual

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

        return request_handler.redirect("%s/%s/%s" % (self.base_url, context.node.id, context.node.redirect))
