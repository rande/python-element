class FlaskActionLoader(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def load_action(self, event):
        container = event.get('container')
        flask = container.get('ioc.extra.flask.app')
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

                flask.add_url_rule(
                    "%s%s%s" % (self.base_url, node.id, settings['path']), 
                    endpoint=name,
                    view_func=container.get('element.flask.view.action').dispatch,
                    methods=settings['methods'],
                    defaults=settings['defaults']
                )        
