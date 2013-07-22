import element.handlers

class PostHandler(element.handlers.NodeHandler):
    
    def get_defaults(self, node):
        return {
            'template': 'element.plugins.blog:post.html'
        }

    def get_name(self):
        return 'Post (Blog)'

    def execute(self, context, flask):
        params = {
            'context': context,
        }

        return flask.make_response(flask.render_template(context.settings['template'], **params))