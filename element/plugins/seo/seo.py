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
        params = {
            'context': context,
            'seo': context.node.seo
        }

        return self.render(request_handler, self.templating, context.settings['template'], params)

    def listener(self, event):
        if 'seo' not in event.get('subject').data:
            return

        node = element.node.Node('seo://%s' % event.get('subject').id, {
            'type': 'seo.headers',
            'seo': event.get('subject').data['seo'],
        })

        event.set('node', node)