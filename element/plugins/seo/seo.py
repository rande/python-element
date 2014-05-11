import element.node

class SeoHandler(element.node.NodeHandler):
    def __init__(self, templating):
        self.templating = templating

    def get_defaults(self, node):
        return {
            'template': 'element.plugins.seo:headers.html'
        }

    def get_name(self):
        return 'Seo'

    def execute(self, request_handler, context):
        return self.render(request_handler, self.templating, context.settings['template'], {
            'context': context,
            'seo': context.seo
        })

    def listener(self, event):
        """
        listen to element.seo.headers event and return a node with seo information only
        subject should be a NodeContext object
        """
        if 'seo' not in event.get('subject').settings:
            return

        node = element.node.Node('seo://%s' % event.get('subject').id, {
            'type': 'seo.headers',
            'seo': event.get('subject').seo,
        })

        event.set('node', node)