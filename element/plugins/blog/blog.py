import element.node

class PostHandler(element.node.NodeHandler):
    def get_defaults(self, node):
        return {
            'template': 'element.plugins.blog:post.html'
        }

    def get_name(self):
        return 'Post (Blog)'

    def execute(self, request_handler, context):

        return 200, context.settings['template'], {
            'context': context,
        }