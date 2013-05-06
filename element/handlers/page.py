import markdown, os
import element.handlers
import datetime

class PageHandler(element.handlers.NodeHandler):
    
    def get_defaults(self, node):
        return {
            'template': 'handlers/page/default.html'
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
