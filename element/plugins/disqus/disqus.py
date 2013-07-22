import element.node

class DisqusHandler(element.node.NodeHandler):
    def __init__(self, account):
        self.account = account

    def get_defaults(self, node):
        return {
            'template': 'element.plugins.disqus:comments.html'
        }

    def get_name(self):
        return 'Disqus'

    def execute(self, context, flask):
        if not self.account:
            return flask.make_response("")

        params = {
            'account': self.account,
        }

        return flask.make_response(flask.render_template(context.settings['template'], **params))

    def listener(self, event):
        node = element.node.Node('disqus://%s' % event.get('subject').id, 'disqus.comments')
        event.set('node', node)