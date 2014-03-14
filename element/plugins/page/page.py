import markdown, os
import element.node

class PageHandler(element.node.NodeHandler):
    def __init__(self, templating):
        self.templating = templating

    def get_name(self):
        return 'Page'

    def get_defaults(self, node):
        return {
            'template': 'element.plugins.page:default.html'
        }

    def execute(self, request_handler, context):
        content = context.node.content
        if context.node.format == 'markdown':
            content = markdown.markdown(context.node.content, ['tables'])

        params = {
            'context': context, 
            'content': content,
        }

        self.render(request_handler, self.templating, context.settings['template'], params)
