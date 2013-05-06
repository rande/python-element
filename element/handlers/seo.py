import element.handlers
import element.node

class SeoHandler(element.handlers.NodeHandler):
    def get_defaults(self, node):
        return {
            'template': 'handlers/seo/headers.html'
        }

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