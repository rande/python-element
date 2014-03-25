import element.node

class DisqusHandler(element.node.NodeHandler):
    def __init__(self, account, templating):
        self.account = account
        self.templating = templating

    def get_defaults(self, node):
        return {
            'template': 'element.plugins.disqus:comments.html'
        }

    def get_name(self):
        return 'Disqus'

    def execute(self, request_handler, context):
        if not self.account:
            return

        params = {
            'account': self.account,
        }

        self.render(request_handler, self.templating, context.settings['template'], params)

    def listener(self, event):
        node = element.node.Node('disqus://%s' % event.get('subject').id, {
            'type': 'disqus.comments',
        })

        event.set('node', node)