import markdown, os
import element.handlers
import datetime

class PostHandler(element.handlers.NodeHandler):
    
    def get_defaults(self, node):
        return {
            'template': 'element:handlers/blog/post.html'
        }

    def execute(self, context, flask):

        content = context.node.content
        if context.node.format == 'markdown':
            content = markdown.markdown(context.node.content)

        params = {
            'context': context, 
            'content': content,
        }

        return flask.make_response(flask.render_template(context.settings['template'], **params))
