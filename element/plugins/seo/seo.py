import element.node

class SeoHandler(element.node.NodeHandler):
    def get_defaults(self, node):
        return {
            'template': 'element.plugins.seo:headers.html'
        }

    def get_name(self):
        return 'Seo'

    def execute(self, context, flask):
        params = {
            'context': context,
            'seo': context.node.seo
        }

        return flask.make_response(flask.render_template(context.settings['template'], **params))

    def listener(self, event):
        if 'seo' not in event.get('subject').data:
            return

        node = element.node.Node('seo://%s' % event.get('subject').id, 'seo.headers', {
            'seo': event.get('subject').data['seo'],
        })

        event.set('node', node)