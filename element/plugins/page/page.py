import markdown, os
import element.node

class PageHandler(element.node.NodeHandler):
    def __init__(self, templating, formatter):
        self.templating = templating
        self.formatter = formatter

    def get_name(self):
        return 'Page'

    def get_defaults(self, node):
        return {
            'template': 'element.plugins.page:default.html'
        }

    def execute(self, request_handler, context):
        self.render(request_handler, self.templating, context.settings['template'], {
            'context': context,
            'content': self.formatter.format(context.node.content, formatter=context.node.format),
        })
