import element.node

class PostHandler(element.node.NodeHandler):

    def __init__(self, templating):
        self.templating = templating

    def get_defaults(self, node):
        return {
            'template': 'element.plugins.blog:post.html'
        }

    def get_name(self):
        return 'Post (Blog)'

    def execute(self, request_handler, context):
        params = {
            'context': context,
        }

        self.render(request_handler, self.templating, context.settings['template'], params)